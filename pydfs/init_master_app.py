import os
import sys  # TODO: remove it
from datetime import datetime
import random

from flask import Flask, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import session
import requests


sys.path.append(".")
from pydfs.logger import _logger  # noqa: E402

app = Flask(__name__)
api = Api(app)

# database
# TODO: maybe add successful messages in logger
# TODO: come up with behaviour when db already exists
# TODO: add db admin user with password
# TODO: create normal workflow if slave IP already in db
_logger.info("creating master.sqlite in ~/.pydfs")
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


@app.route('/post')
def post():

    file = request.args.get('path')
    node_id = random.randrange(start=1, stop=2, step=1)

    save_node = session.query(Slave).filter(Slave.id == node_id).one()
    requests.post(url=f"http/{save_node.ip}/.pydfs", data=file)


@app.route('/get')
def get():

    file_name = request.args.get('path')

    for node_id in range(1, 2):

        save_node = session.query(Slave).filter(Slave.id == node_id).one()
        response = requests.get(url=f"http/{save_node.ip}/.pydfs/{file_name}")

        if int(response.status_code) == 200:  # TODO: not sure about this
            return response

    _logger.info(f"File {file_name} wasn't found")
