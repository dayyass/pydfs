import sys  # TODO: remove it

import requests  # type: ignore

sys.path.append(".")
from pydfs.logger import _logger  # noqa: E402
from pydfs.utils import ping, mkdir_pydfs  # noqa: E402


# TODO: make daemon from it
def cmd_init_master() -> None:
    """
    pydfs init master
    """

    # TODO: maybe move it up
    # TODO: validate if import is correct
    from pydfs.flask_init_master import app  # noqa: E402

    _logger.info("master node initialized successfully")
    app.run(debug=True)  # TODO: remove debug


# TODO: think how to match existed slave to master
# TODO: check if master and slave are already connected
def cmd_init_slave(master_ip: str) -> None:
    """
    pydfs init slave --master_ip ...

    Args:
        master_ip (str): pydfs master node IP.
    """

    # TODO: maybe change order
    mkdir_pydfs()
    _ping_master_node(master_ip=master_ip)
    _send_slave_ip_to_master(master_ip=master_ip)


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
        f"http://{master_ip}:5000/add_slave_node",
        data={},  # TODO: validate
    )

    if response.status_code == 200:
        _logger.info("slave node initialized successfully")
    else:
        try:  # TODO: fix try/except block
            _logger.debug(f"response json keys: {response.json().keys()}")
            err_msg = f"HTTP {response.status_code}: {response.json()['message']}"
        except:  # noqa: E722
            _logger.debug("response doesn't have json in it")
            err_msg = f"HTTP {response.status_code}"

        # TODO: maybe warning, not error
        _logger.error(f"{err_msg}\nslave node was NOT initialized successfully")
        raise requests.HTTPError(err_msg)
