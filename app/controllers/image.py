"""
Controller responsible for manipulate the images
"""
import os
import requests
from http import HTTPStatus
from flask import Blueprint, jsonify, current_app, request

bp_image = Blueprint(name=__name__, import_name=__name__)

@bp_image.route("/images/<filename>", methods=["GET"])
def retrieve_image(filename):
    """
    Blueprint method to get one image from the server
    """
    return jsonify({}), HTTPStatus.OK


@bp_image.route("/draw/", methods=["POST"])
def draw_text_box():
    # get json
    json_data = request.get_json()
    print(json_data)

    # download image
    img_url = json_data['image_url']
    download_img(img_url)

    return jsonify({}), HTTPStatus.OK

def download_img(url):
    img_name = os.path.basename(url)
    img_dir = current_app.config["IMAGES_DIR"]
    abs_path = os.path.join(img_dir, img_name)
    with open(abs_path, 'wb') as handle:
            response = requests.get(url, stream=True)
            if not response.ok:
                print('Unable to get image')

            for block in response.iter_content(1024):
                if not block: break
                handle.write(block)