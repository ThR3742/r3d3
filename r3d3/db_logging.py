import datetime
import os
import pandas as pd
from .experiment_db import ExperimentDB


class R3D3Logger(object):
    def __init__(self, db_path):
        self.experiment_db = ExperimentDB(db_path=db_path)
        self.experiment_db.init_experiment_table(drop=False)
        self.experiment_db.init_logging_table(drop=False)

    def do_log(self, experiment_id, run_id, level, message):
        with self.experiment_db.db_cursor() as cur:
            ts = datetime.datetime.now().timestamp()

            cur.execute(
                f"""INSERT INTO logging VALUES (
                {experiment_id},
                {run_id},
                {ts},
                '{os.environ.get("USER", "unknown")}',
                '{level}',
                '{message}'
            )
            """
            )

    def info(self, experiment_id, run_id, message):
        self.do_log(experiment_id, run_id, "INFO", message)

    def debug(self, experiment_id, run_id, message):
        self.do_log(experiment_id, run_id, "DEBUG", message)

    def error(self, experiment_id, run_id, message):
        self.do_log(experiment_id, run_id, "ERROR", message)

    def warning(self, experiment_id, run_id, message):
        self.do_log(experiment_id, run_id, "WARNING", message)

    def get_full_log(self, experiment_id, run_id):
        with self.experiment_db.db_cursor() as cur:
            ret = list()
            for row in cur.execute(
                f"""
                SELECT * FROM logging
                WHERE run_id = '{run_id}' 
                AND experiment_id = '{experiment_id}'
                """
            ):
                ret.append(row)

            return pd.DataFrame(
                data=ret,
                columns=["experiment_id", "run_id", "timestamp", "owner", "level", "message"],
            )
