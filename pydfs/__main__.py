# TODO: remove it
import sys

sys.path.append(".")
from pydfs.arg_parse import parse_args  # noqa: E402
from pydfs.cmd_init import cmd_init_master, cmd_init_slave  # noqa: E402
from pydfs.logger import _logger  # noqa: E402


def main() -> None:
    """
    pydfs main function (entry point)
    """

    args = parse_args()
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


if __name__ == "__main__":
    main()
