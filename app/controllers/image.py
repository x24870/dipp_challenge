"""
Controller responsible for manipulate the images
"""
from http import HTTPStatus
from flask import Blueprint, jsonify

bp_image = Blueprint(name=__name__, import_name=__name__)


@bp_image.route("/images/<filename>", methods=["GET"])
def retrieve_image(filename):
    """
    Blueprint method to get one image from the server
    """
    return jsonify({}), HTTPStatus.OK


@bp_image.route("/draw", methods=["POST"])
def draw_text_box():
    """
    Blueprint method to draw a text box on the image
    """
    return jsonify({}), HTTPStatus.OK
