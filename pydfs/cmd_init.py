import os

import requests  # type: ignore

from pydfs.logger import _logger  # noqa: E402
from pydfs.utils import ping  # noqa: E402


# TODO: make daemon from it
def cmd_init_master() -> None:
    """
    pydfs init master
    """

    _mkdir_pydfs()

    # TODO: maybe move it up
    # TODO: validate if import is correct
    from pydfs.master_app import app  # noqa: E402

    _logger.info("master node initialized successfully")

    # TODO: add WSGI (e.g. gunicorn)
    # TODO: remove host="0.0.0.0"
    app.run(host="0.0.0.0")


# TODO: think how to match existed slave to master
# TODO: check if master and slave are already connected
def cmd_init_slave(master_ip: str) -> None:
    """
    pydfs init slave --master_ip ...

    Args:
        master_ip (str): pydfs master node IP.
    """

    # TODO: maybe change order
    _mkdir_pydfs()
    # _ping_master_node(master_ip=master_ip)  # TODO: fix with docker-compose
    _send_slave_ip_to_master(master_ip=master_ip)

    # TODO: maybe move it up
    # TODO: validate if import is correct
    from pydfs.slave_app import app  # noqa: E402

    _logger.info("slave node initialized successfully")

    # TODO: add WSGI (e.g. gunicorn)
    # TODO: remove host="0.0.0.0"
    app.run(host="0.0.0.0")


def _mkdir_pydfs() -> None:
    """
    Create pydfs working directory ~/.pydfs
    """

    path = os.path.join(os.environ["HOME"], ".pydfs")
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=False)
        _logger.info(f"'{path}' folder created")
    else:
        # TODO: think about workflow (behaviour)
        _logger.info(f"'{path}' folder has already been created")


# TODO: save pydfs init info, for example master_ip for slave nodes
def _ping_master_node(master_ip: str) -> None:
    """
    Function to ping master node by its IP.

    Args:
        master_ip (str): pydfs master node IP.
    """

    if ping(master_ip):
        _logger.info(f"master node '{master_ip}' was found")
    else:
        # TODO: make more informative error message
        err_msg = f"master node '{master_ip}' was not found"
        _logger.error(err_msg)
        raise ConnectionError(err_msg)


def _send_slave_ip_to_master(master_ip: str) -> None:
    """
    Function to sent slave node IP to master node.

    Args:
        master_ip (str): pydfs master node IP.
    """

    # TODO: add https
    # TODO: remove port hardcode (parametrize)
    # TODO: maybe post request, not put
    # TODO: send local api for validation
    response = requests.put(
        f"http://{master_ip}:5000/add_slave",
        data={},  # TODO: validate
    )

    if response.status_code == 200:
        _logger.info("successfully send ip to master")
    else:
        try:  # TODO: fix try/except block
            _logger.debug(f"response json keys: {response.json().keys()}")
            err_msg = f"HTTP {response.status_code}: {response.json()['message']}"
        except:  # noqa: E722
            _logger.debug("response doesn't have json in it")
            err_msg = f"HTTP {response.status_code}"

        # TODO: maybe warning, not error
        _logger.error(f"{err_msg}: slave node was NOT initialized successfully")
        raise requests.HTTPError(err_msg)
