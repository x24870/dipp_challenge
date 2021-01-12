"""
Controller responsible for manipulate the images
"""
import os, re

import requests
from http import HTTPStatus
from flask import Blueprint, jsonify, current_app, request, send_file

from .resp import APIResponse
from .image_helper import *

bp_image = Blueprint(name=__name__, import_name=__name__)

@bp_image.route("/images/<filename>", methods=["GET"])
def retrieve_image(filename):
    img_dir = current_app.config["IMAGES_DIR"]
    if filename not in os.listdir(img_dir):
        return APIResponse.not_found()
    
    abs_apth = os.path.join(img_dir, filename)
    return send_file(abs_apth)

@bp_image.route("/draw/", methods=["POST"])
def draw_text_box():
    # validate json data
    json_data = request.get_json()
    is_valid, status = validate_params(json_data)
    if not is_valid: return status

    # download image
    img_path = download_img(json_data['image_url'])
    if img_path == None: return APIResponse.unable_fetch_file()

    #download font
    font_path = download_font(json_data['font_url'])
    if font_path == None: return APIResponse.unable_fetch_file()

    # generate response json
    box = json_data['box']
    text = json_data['text']
    json_resp = gen_resp_json(img_path, font_path, box, text)
    if json_resp['splits'] == None: return APIResponse.unable_fit_content()

    # draw text and border
    colors = (text['border_color'], text['text_color'])
    draw_content(img_path, font_path, box, colors, json_resp)
    
    return APIResponse.success(json_resp)
