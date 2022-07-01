import os

from logger import _logger


def cmd_init_master() -> None:
    """
    pydfs init master
    """

    _logger.info("master node initialized successfully")


def cmd_init_slave(master_ip: str) -> None:
    """
    pydfs init slave

    Args:
        master_ip (str): pydfs master node IP.
    """

    # ping master node
    # TODO: save pydfs init info, for example master_ip for slave nodes
    if _ping(master_ip):
        _logger.info(f"master node '{master_ip}' was found")
    else:
        # TODO: make more informative error message
        err_msg = f"master node '{master_ip}' was not found"
        _logger.error(err_msg)
        raise ConnectionError(err_msg)

    # mkdir ~/.pydfs
    path = os.path.join(os.environ["HOME"], ".pydfs")
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=False)
        _logger.info(f"'{path}' folder created")
    else:
        _logger.info(f"'{path}' folder has already been created")

    _logger.info("slave node initialized successfully")


# TODO: use with IP
# TODO: validate
def _ping(hostname: str) -> bool:
    """
    https://stackoverflow.com/questions/2953462/pinging-servers-in-python
    """

    cmd = f"ping -c 1 {hostname}"
    _logger.debug(f"ping command: {cmd}")

    response = os.system(cmd)
    success = not bool(response)

    return success
