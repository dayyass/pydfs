import os
from base64 import b64encode

from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy

from pydfs.logger import _logger  # noqa: E402

app = Flask(__name__)
api = Api(app)

# database
# TODO: maybe add successful messages in logger
# TODO: come up with behaviour when db already exists
# TODO: add db admin user with password
# TODO: create normal workflow if slave IP already in db
_logger.info("creating slave.sqlite in ~/.pydfs")
uri = f"sqlite:///{os.path.join(os.environ['HOME'], '.pydfs', 'slave.sqlite')}"

app.config["SQLALCHEMY_DATABASE_URI"] = uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # TODO: validate
db = SQLAlchemy(app)

# TODO: add slave and master file tables
db.create_all()


class PutFileSlave(Resource):
    def put(self):

        _logger.debug(f"request.files: {request.files}")
        _logger.debug(f"receive file: {request.files['upload_file']}")

        request.files["upload_file"].save(
            os.path.join(
                os.environ["HOME"],
                ".pydfs",
                request.files["upload_file"].filename,  # TODO: validate
            ),
        )

        return {}  # TODO: validate


class GetFileSlave(Resource):
    def get(self):

        _logger.debug(f"request args: {request.args}")

        path = request.args["path"]  # TODO: rename filename
        _logger.debug(f"request 'path' param: {path}")

        full_path = os.path.join(
            os.environ["HOME"],
            ".pydfs",
            path,  # TODO: validate
        )
        _logger.debug(f"full path: {full_path}")

        # TODO: maybe not b64encode
        # TODO: close opened file
        return jsonify(
            {
                "download_file": b64encode(open(full_path, mode="rb").read()).decode(
                    "utf-8"
                )
            }
        )


api.add_resource(PutFileSlave, "/put_file")
api.add_resource(GetFileSlave, "/get_file")
