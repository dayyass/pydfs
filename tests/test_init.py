import sys  # TODO: remove it
import threading
import time
import unittest

sys.path.append(".")
from pydfs.__main__ import _main  # noqa: E402
from pydfs.arg_parse import get_argparse  # noqa: E402


# TODO: test different workflows
# TODO: maybe use flask-testing
class TestInit(unittest.TestCase):
    """
    Class for testing pydfs init commands.
    """

    def setUp(self):
        # https://stackoverflow.com/questions/18160078/how-do-you-write-tests-for-the-argparse-portion-of-a-python-module
        self.parser = get_argparse()

    # TODO: test different workflows
    def test_init_master_and_slave(self):

        # init master
        args_master = self.parser.parse_args(["init", "master"])

        # create a thread that will contain running server
        # https://gist.github.com/prschmid/4643738
        master_node_thread = threading.Thread(
            target=_main,
            args=(args_master,),
            daemon=True,  # TODO: check correctness
        )
        master_node_thread.start()
        time.sleep(5)  # TODO: fix hardcode

        # init slave
        args_slave = self.parser.parse_args(
            ["init", "slave", "--master_ip", "127.0.0.1"]
        )
        exit_code = _main(args_slave)
        self.assertEqual(exit_code, 0)


if __name__ == "__main__":
    unittest.main()
