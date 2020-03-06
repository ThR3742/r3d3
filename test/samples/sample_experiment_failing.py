from r3d3 import R3D3ExperimentPlan
from r3d3.rootpath import rootpath
import tempfile

experiment_plan = R3D3ExperimentPlan.from_cartesian_space(
    db_path=tempfile.mkstemp()[1],
    configs={
        "a": [1],
        "b": [3],
        "do_fail": [1]
    },
    binary=f"{rootpath}/test/samples/sample_binary.py",
    max_nb_processes=2
)
