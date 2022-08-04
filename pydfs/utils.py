import os

from pydfs.logger import _logger  # noqa: E402


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
