from r3d3 import R3D3Experiment
from r3d3.rootpath import rootpath
import tempfile

experiment = R3D3Experiment(
    db_path=tempfile.mkstemp()[1],
    configs={
        "a": [1, 2],
        "b": [3, 4]
    },
    binary=f"{rootpath}/test/samples/sample_binary.py",
    max_nb_processes=2
)
