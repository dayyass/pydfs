import sys  # TODO: remove it
import unittest

sys.path.append(".")
from pydfs.__main__ import _main  # noqa: E402
from pydfs.arg_parse import get_argparse  # noqa: E402


class TestInfo(unittest.TestCase):
    """
    Class for testing pydfs --info and pydfs --version.
    """

    def setUp(self):
        # https://stackoverflow.com/questions/18160078/how-do-you-write-tests-for-the-argparse-portion-of-a-python-module
        self.parser = get_argparse()

    def test_version(self):
        args = self.parser.parse_args(["--version"])
        exit_code = _main(args)
        self.assertEqual(exit_code, 0)

    # TODO: test different workflows
    def test_info(self):
        args = self.parser.parse_args(["--info"])
        exit_code = _main(args)
        self.assertEqual(exit_code, 0)


if __name__ == "__main__":
    unittest.main()
