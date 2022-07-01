import os

from logger import _logger


def cmd_init_master() -> None:
    """
    pydfs init --node master
    """

    _logger.info("master node initialized successfully")


def cmd_init_slave() -> None:
    """
    pydfs init --node slave
    """

    path = os.path.join(os.environ["HOME"], ".pydfs")
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=False)
        _logger.info(f"'{path}' folder created")

    _logger.info("slave node initialized successfully")
