import random
from io import BufferedReader
from typing import Dict, List

import requests  # type: ignore

from pydfs.logger import _logger  # noqa: E402


def cmd_dfs_put_request(ip: str, files: Dict[str, BufferedReader]):
    response = requests.put(  # TODO: maybe post
        url=f"http://{ip}:5000/put_file",  # TODO: add https
        files=files,
    )
    if response.status_code == 200:
        _logger.info(f"sending file {files['upload_file']} to {ip} succeeded")
    else:
        _logger.error(f"sending file {files['upload_file']} to {ip} failed")


def cmd_dfs_get_request(ip: str, path: str):
    response = requests.get(
        url=f"http://{ip}:5000/get_file",  # TODO: add https
        params={"path": path},
    )
    if response.status_code == 200:
        _logger.info(f"requesting file {path} from {ip} succeeded")
    else:  # TODO: add error handler
        _logger.error(f"requesting file {path} from {ip} failed")

    # TODO: standartize interface with cmd_dfs_get_request
    # TODO: error handler
    return response


# TODO: add type annotation without cycle import
def _choose_slave_node(
    slave_nodes: List,
):
    slave_node_tgt = random.choice(slave_nodes)
    return slave_node_tgt
