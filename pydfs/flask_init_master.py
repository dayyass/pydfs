import os
import sys  # TODO: remove it
from datetime import datetime

from flask import Flask, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy

sys.path.append(".")
from pydfs.logger import _logger  # noqa: E402

app = Flask(__name__)
api = Api(app)

# database
# TODO: maybe add successful messages in logger
# TODO: come up with behaviour when db already exists
# TODO: add db admin user with password
# TODO: create normal workflow if slave IP already in db
uri = f"sqlite:///{os.path.join(os.environ['HOME'], '.pydfs', 'master.sqlite')}"
app.config["SQLALCHEMY_DATABASE_URI"] = uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # TODO: validate
db = SQLAlchemy(app)


class Slave(db.Model):  # type: ignore

    __tablename__ = "slave"  # TODO: check the need
    # __table_args__ = {"extend_existing": True}  # TODO: check it

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ip_address = db.Column(db.String(15), unique=True, nullable=False)
    timestamp = db.Column(db.String(23), unique=False, nullable=False)

    def __repr__(self):
        return f"<Slave {self.ip_address}>"


_logger.info("creating master.sqlite in ~/.pydfs")
_logger.info("creating slave table in master.sqlite")
db.create_all()


class AddSlave(Resource):
    def put(self):
        # https://stackoverflow.com/questions/3759981/get-ip-address-of-visitors-using-flask-for-python
        _logger.info(
            f"inserting slave node address {request.remote_addr} in master.sqlite"
        )

        slave = Slave(
            ip_address=request.remote_addr,
            timestamp=datetime.now().strftime(r"%Y-%m-%d %H:%M:%S.%f")[:-3],
        )
        db.session.add(slave)
        db.session.commit()

        return {}  # TODO: validate


api.add_resource(AddSlave, "/add_slave")
