import argparse
import os
from base64 import b64decode

from pydfs import __version__  # noqa: E402
from pydfs.arg_parse import get_argparse  # noqa: E402
from pydfs.cmd_dfs import cmd_dfs_get_request, cmd_dfs_put_request  # noqa: E402
from pydfs.cmd_init import cmd_init_master, cmd_init_slave  # noqa: E402
from pydfs.logger import _logger  # noqa: E402


def main() -> None:
    """
    pydfs main function (entry point)
    """

    args = get_argparse().parse_args()
    _main(args)


def _main(args: argparse.Namespace) -> int:
    """
    pydfs main function (entry point)

    Args:
        args (argparse.Namespace): CLI arguments.

    Returns:
        int: exit code.
    """

    if args.version and (not args.command):
        _version()
        return 0

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
            _logger.info(
                f"pydfs dfs put --path {args.path} --master_ip {args.master_ip}"
            )
            cmd_dfs_put_request(
                ip=args.master_ip,
                files={"upload_file": open(args.path, mode="rb")},
            )
            # TODO add error handler
            _logger.info(f"putting file {args.path} to pydfs succeeded")

        elif args.subcommand == "get":
            _logger.info(
                f"pydfs dfs get --path {args.path} --master_ip {args.master_ip}"
            )
            response = cmd_dfs_get_request(
                ip=args.master_ip,
                path=args.path,
            )

            _logger.info(f"slave response on user: {response}")

            file = b64decode(response.json()["download_file"])
            with open(args.path, mode="wb") as fp:
                fp.write(file)

            # TODO add error handler
            _logger.info(f"getting and saving file {args.path} from pydfs succeeded")

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


def _version() -> None:
    """
    pydfs --version
    """

    # TODO: maybe not use print
    print(f"v{__version__}")


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
    main()
