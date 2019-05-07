import tempfile

DB_PATH = tempfile.mkstemp()[1]

CONFIGS = {
    "a": [1, 2],
    "b": [3, 4]
}

BINARY = "test/samples/sample_binary.py"

MAX_NB_PROCESSES = 2