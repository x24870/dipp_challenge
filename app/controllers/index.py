"""
Controller responsible for managing the API index
"""
from http import HTTPStatus
from flask import Blueprint, jsonify

bp_index = Blueprint(name=__name__, import_name=__name__)


@bp_index.route("/", methods=["GET"])
def api_index():
    """
    Blueprint method to return the API index
    """
    json_resp = {
        "code": HTTPStatus.OK,
        "message": "Welcome to Dipp's code challenge.",
    }

    return jsonify(json_resp), HTTPStatus.OK
