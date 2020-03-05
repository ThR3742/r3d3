from r3d3 import R3D3ExperimentPlan
from r3d3.rootpath import rootpath
import tempfile

experiment_plan_1 = R3D3ExperimentPlan.from_cartesian_space(
    db_path=tempfile.mkstemp()[1],
    configs={"a": [1, 2], "b": [3, 4]},
    binary=f"{rootpath}/test/samples/sample_binary.py",
    max_nb_processes=2,
)

experiment_plan_2 = R3D3ExperimentPlan.from_cartesian_space(
    db_path=tempfile.mkstemp()[1],
    configs={"a": [1, 2], "b": [3, 4]},
    binary=f"{rootpath}/test/samples/sample_binary.py",
    max_nb_processes=2,
)

experiment_plan = R3D3ExperimentPlan.from_multiple_plans(
    [experiment_plan_1, experiment_plan_2]
)
