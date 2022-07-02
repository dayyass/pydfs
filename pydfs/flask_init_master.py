import os
import sqlite3
import sys  # TODO: remove it
from datetime import datetime

from flask import Flask, request
from flask_restful import Api, Resource  # TODO: maybe use just flask

sys.path.append(".")
from pydfs.logger import _logger  # noqa: E402

app = Flask(__name__)
api = Api(app)

# database
# TODO: use ORM
# TODO: add datetime column
# TODO: maybe add successful messages
# TODO: come up with behaviour when db already exists
# TODO: maybe parametrize db address
# TODO: remove check_same_thread=False
_logger.info("creating master.sqlite")
conn = sqlite3.connect(
    os.path.join(os.environ["HOME"], ".pydfs", "master.sqlite"),
    check_same_thread=False,
)
cur = conn.cursor()

_logger.info("creating slave table in master.sqlite")
# TODO: remove hotfix IF NOT EXISTS
# TODO: create normal workflow if slave IP already in db
cur.execute(
    """
    CREATE TABLE IF NOT EXISTS slave (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        remote_address TEXT NOT NULL UNIQUE,
        datetime TEXT NOT NULL
    )
    """
)


class AddSlaveNode(Resource):
    def put(self):
        # https://stackoverflow.com/questions/3759981/get-ip-address-of-visitors-using-flask-for-python
        _logger.info(
            f"inserting slave node address {request.remote_addr} in master.sqlite"
        )

        # https://stackoverflow.com/questions/17227110/how-do-datetime-values-work-in-sqlite
        cur.execute(
            """
            INSERT INTO slave (remote_address, datetime)
            VALUES (:addr, :timestamp)
            """,
            {
                "addr": request.remote_addr,
                "timestamp": datetime.now().strftime(r"%Y-%m-%d %H:%M:%S.%f")[:-3],
            },
        )
        conn.commit()
        return {}  # TODO: validate


api.add_resource(AddSlaveNode, "/add_slave_node")
