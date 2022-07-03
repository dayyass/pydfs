import argparse
import os
import sys  # TODO: remove it

sys.path.append(".")
from pydfs.arg_parse import get_argparse  # noqa: E402
from pydfs.init import cmd_init_master, cmd_init_slave  # noqa: E402
from pydfs.logger import _logger  # noqa: E402


def main(args: argparse.Namespace) -> int:
    """
    pydfs main function (entry point)

    Args:
        args (argparse.Namespace): CLI arguments.

    Returns:
        int: exit code.
    """

    if args.info and (not args.command):
        _info()
        return 0

    _logger.debug(f"CLI arguments: {args}")

    if args.command == "init":

        if args.subcommand == "master":
            _logger.info(f"pydfs init {args.subcommand}")
            cmd_init_master()

        elif args.subcommand == "slave":
            _logger.info(f"pydfs init {args.subcommand} --master_ip {args.master_ip}")
            cmd_init_slave(master_ip=args.master_ip)

        else:
            err_msg = f"unknown init subcommand: '{args.subcommand}' (use 'master' or 'slave')"
            _logger.error(err_msg)
            raise ValueError(err_msg)

    elif args.command == "dfs":

        if args.subcommand == "put":
            _logger.info(f"pydfs dfs put --path {args.path}")
            # TODO

        elif args.subcommand == "get":
            _logger.info(f"pydfs dfs get --path {args.path}")
            # TODO

        else:
            err_msg = (
                f"unknown dfs subcommand: '{args.subcommand}' (use 'put' or 'get')"
            )
            _logger.error(err_msg)
            raise ValueError(err_msg)

    else:
        err_msg = f"unknown command: '{args.command}' (use 'init' or 'dfs')"
        _logger.error(err_msg)
        raise ValueError(err_msg)

    return 0


def _info() -> None:
    """
    pydfs --info
    """

    path_to_pydfs = os.path.join(os.environ["HOME"], ".pydfs")
    path_to_master_db = os.path.join(path_to_pydfs, "master.sqlite")

    # TODO: maybe not use print
    # TODO: maybe allow master and slave node at the same time
    if os.path.exists(path_to_master_db):
        # TODO: add slave nodes info
        print("pydfs master node\n")
    elif os.path.exists(path_to_pydfs):
        # TODO: add master node info
        print("pydfs slave node\n")
    else:
        msg = (
            "not a pydfs node\n"
            "init it as a master node with `pydfs init master` or\n"
            "init it as a slave node with `pydfs init slave --master_ip [IP]`\n"
        )
        print(msg)


if __name__ == "__main__":
    args = get_argparse().parse_args()
    main(args)
