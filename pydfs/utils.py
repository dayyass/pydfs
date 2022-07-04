import os
import sys  # TODO: remove it

sys.path.append(".")
from pydfs.logger import _logger  # noqa: E402


def mkdir_pydfs() -> None:
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


# TODO: use with IP
# TODO: validate
# TODO: maybe rename hostname
def ping(hostname: str) -> bool:
    """
    https://stackoverflow.com/questions/2953462/pinging-servers-in-python
    """

    cmd = f"ping -c 1 {hostname}"
    _logger.debug(f"ping command: {cmd}")

    response = os.system(cmd)
    _logger.debug(f"ping response code: {response}")

    success = not bool(response)

    return success
