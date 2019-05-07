import argparse
import sys
import os
from concurrent.futures import ThreadPoolExecutor
import subprocess
from datetime import datetime
import time
import typing

from r3d3.utils import cartesian_product
from r3d3.experiment_db import ExperimentDB

root_dir = "{}/..".format(os.path.dirname(os.path.abspath(__file__)))


class ExperimentLauncher(object):

    def __init__(self, db_path):
        self.db = ExperimentDB(db_path)

    def run(self, binary: str, configs: typing.List, max_nb_processes: int):
        self.db.init_experiment_table()

        def launcher_with_environment(env, debug):
            def launch_command_line(command):
                tab = command.split()
                print("Executing {}".format(command))
                if not debug:
                    print(tab)
                    try:
                        myPopen = subprocess.Popen(
                            tab,
                            env=env,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
                        for l in myPopen.stderr:
                            print(l)
                    except subprocess.CalledProcessError as e:
                        print(e.output)

            return launch_command_line

        # Creating env for the runs
        env = os.environ.copy()
        print("Using env {}".format(env))

        nb_tests = len(configs)
        print("%d experiments to launch..." % nb_tests)

        # Creating executors with max nb processes from the config
        executor = ThreadPoolExecutor(max_workers=max_nb_processes)

        # Running the tests
        now = datetime.now()
        experiment_id = int(time.mktime(now.timetuple()))

        for run_id, parameter_set in enumerate(configs):
            # The python binary is available in sys.executable
            args = ["{} {}".format(sys.executable, "{}/{}".format(root_dir, binary))]
            for a in parameter_set:
                args.append("-" + a + " " + str(parameter_set[a]))
            args.append(f"--run_id {run_id}")
            # The experiment should be aware of the number of running processes so that it does not
            # ask for too much memory on the GPU
            args.append("--max_nb_processes {}".format(min([max_nb_processes, nb_tests])))
            args.append(f"--experiment_id {experiment_id}")

            self.db.add_experiment(
                experiment_id=experiment_id,
                run_id=run_id,
                config=parameter_set
            )

            command = " ".join(args)
            executor.submit(launcher_with_environment(env, debug=False), command)


def main(experiment_file: str):
    print(experiment_file)

    variables = dict()
    with open(experiment_file) as f:
        exec(f.read(), variables)

    my_launcher = ExperimentLauncher(variables["DB_PATH"])
    my_configs = cartesian_product(variables["CONFIGS"])
    my_launcher.run(variables["BINARY"], my_configs, variables["MAX_NB_PROCESSES"])

    return my_launcher


def main_cli():
    parser = argparse.ArgumentParser(description='Experiment Launcher')
    parser.add_argument('--experiment_file', type=str)
    args = parser.parse_args()

    main(
        experiment_file=args.experiment_file
    )

