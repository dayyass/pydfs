import argparse


def parse_args() -> argparse.Namespace:
    """
    Function to get CLI arguments.

    Returns:
        argparse.Namespace: CLI arguments.
    """

    # TODO: add --version argument
    # TODO: add --info argument
    parser = argparse.ArgumentParser()

    # https://stackoverflow.com/questions/8250010/argparse-identify-which-subparser-was-used
    subparsers = parser.add_subparsers(dest="command")

    # init commands
    subparser_init = subparsers.add_parser(
        "init",
        help="init commands",
    )
    subsubparsers_init = subparser_init.add_subparsers(dest="subcommand")

    # init master command
    subsubparsers_init.add_parser(
        "master",
        help="init pydfs master node",
    )

    # init slave command
    subsubparser_init_slave = subsubparsers_init.add_parser(
        "slave",
        help="init pydfs slave node",
    )
    subsubparser_init_slave.add_argument(
        "--master_ip",
        type=str,
        required=True,
        help="pydfs master node IP",
    )

    # dfs commands
    subparser_dfs = subparsers.add_parser(
        "dfs",
        help="dfs commands",
    )
    subsubparsers_dfs = subparser_dfs.add_subparsers(dest="subcommand")

    # dfs put command
    subsubparser_dfs_put = subsubparsers_dfs.add_parser(
        "put",
        help="command to put local file in pydfs",
    )
    subsubparser_dfs_put.add_argument(
        "--path",
        type=str,
        required=True,
        help="path to local file to put in pydfs",
    )

    # dfs get command
    subsubparser_dfs_get = subsubparsers_dfs.add_parser(
        "get",
        help="command to get pydfs file back to local",
    )
    subsubparser_dfs_get.add_argument(
        "--path",
        type=str,
        required=True,
        help="path to pydfs file to get it locally",
    )

    return parser.parse_args()
