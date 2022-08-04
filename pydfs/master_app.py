import os
from datetime import datetime

from flask import Flask, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy

from pydfs.cmd_dfs import (  # noqa: E402
    _choose_slave_node,
    cmd_dfs_get_request,
    cmd_dfs_put_request,
)
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


# TODO: link (relation) with Slave table by ip_address
class Files(db.Model):  # type: ignore

    __tablename__ = "files"  # TODO: check the need
    # __table_args__ = {"extend_existing": True}  # TODO: check it

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # TODO: fix 255 length
    filename = db.Column(db.String(255), unique=True, nullable=False)
    ip_address = db.Column(db.String(15), unique=True, nullable=False)
    timestamp = db.Column(db.String(23), unique=False, nullable=False)

    def __repr__(self):
        return f"<File {self.filename} at {self.ip_address}>"


_logger.info("creating files table in master.sqlite")


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


class PutFileMaster(Resource):
    def put(self):

        _logger.debug(f"request.files: {request.files}")
        _logger.debug(f"receive file: {request.files['upload_file']}")

        slave_nodes = Slave.query.all()
        _logger.debug(f"available slave nodes: {slave_nodes}")

        slave_node_tgt = _choose_slave_node(slave_nodes=slave_nodes)
        _logger.debug(f"chosen slave node: {slave_node_tgt}")

        file = request.files["upload_file"]

        # TODO: add redirect
        # TODO: make as a transaction
        # https://stackoverflow.com/questions/32460524/post-uploaded-file-using-requests
        cmd_dfs_put_request(
            ip=slave_node_tgt.ip_address,
            files={"upload_file": (file.filename, file.stream, file.mimetype)},
        )

        # TODO add error handler
        file_db = Files(
            filename=file.filename,
            ip_address=slave_node_tgt.ip_address,
            timestamp=datetime.now().strftime(r"%Y-%m-%d %H:%M:%S.%f")[:-3],
        )
        db.session.add(file_db)
        db.session.commit()

        return {}  # TODO: validate


class GetFileMaster(Resource):
    def get(self):

        _logger.debug(f"request args: {request.args}")

        path = request.args["path"]  # TODO: rename filename
        _logger.debug(f"request 'path' param: {path}")

        _logger.info(f"getting slave node ip with file: {path}")
        files = Files.query.filter_by(filename=path).all()
        assert len(files) == 1  # TODO: remove and create good error handler
        slave_node_tgt_ip_address = files[0].ip_address

        # TODO: add redirect
        # TODO: make as a transaction
        # https://stackoverflow.com/questions/32460524/post-uploaded-file-using-requests
        response = cmd_dfs_get_request(
            ip=slave_node_tgt_ip_address,
            path=path,
        )

        _logger.info(f"slave response on master: {response}")

        return response.json()


api.add_resource(AddSlave, "/add_slave")
api.add_resource(PutFileMaster, "/put_file")
api.add_resource(GetFileMaster, "/get_file")
