from arg_parse import parse_args
from logger import _logger

if __name__ == "__main__":

    args = parse_args()
    _logger.info(f"CLI arguments: {args}")

    if args.command == "init":

        if args.node == "master":
            _logger.info(f"pydfs init --node {args.node}")
            # TODO

        elif args.node == "slave":
            _logger.info(f"pydfs init --node {args.node}")
            # TODO

        else:
            err_msg = (
                f"unknown init --node argument: '{args.node}' (use 'master' or 'slave')"
            )
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
        raise ValueError(err_msg)  # TODO: move into arg_parse
