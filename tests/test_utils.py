import sys  # TODO: remove it
import unittest

sys.path.append(".")
from pydfs.utils import ping  # noqa: E402


class TestUtils(unittest.TestCase):
    """
    Class for testing utils.
    """

    def test_ping(self):
        self.assertTrue(ping("localhost"))
        self.assertTrue(ping("127.0.0.1"))
        self.assertFalse(ping("127001"))


if __name__ == "__main__":
    unittest.main()
