import tempfile
import unittest
import os

from r3d3.db_logging import R3D3Logger


class TestDBLogging(unittest.TestCase):
    def test_logging(self):
        db_path = tempfile.mkstemp()[1]
        print(db_path)
        logger = R3D3Logger(db_path)

        logger.info(1, 1, "Hello")
        logger.error(1, 1, "Some error")
        logger.debug(1, 1, "Some debug")
        logger.warning(1, 1, "Some warning")

        print(logger.get_full_log(1, 1))

        os.remove(db_path)
