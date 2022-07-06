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
_logger.info("creating master.sqlite in ~/.pydfs")
uri = f"sqlite:///{os.path.join(os.environ['HOME'], '.pydfs', 'master.sqlite')}"

app.config["SQLALCHEMY_DATABASE_URI"] = uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # TODO: validate
db = SQLAlchemy(app)


# TODO: maybe rewrite inheritance into repository and remain only class with fields and methods?
# TODO: fix class structue because it's just a copypaste of Slave class
class Master(db.Model):  # type: ignore

    __tablename__ = "master"  # TODO: check the need
    # __table_args__ = {"extend_existing": True}  # TODO: check it

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ip_address = db.Column(db.String(15), unique=True, nullable=False)
    timestamp = db.Column(db.String(23), unique=False, nullable=False)

    def __repr__(self):
        return f"<Master {self.ip_address}>"
