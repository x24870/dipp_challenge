"""
Controller responsible for manipulate the images
"""
import os
import requests
from http import HTTPStatus
from flask import Blueprint, jsonify, current_app, request
from PIL import ImageFont, ImageDraw, Image

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
    # print(json_data)

    # download image
    img_url = json_data['image_url']
    img_path = download_img(img_url)

    # calculate font size and split text
    box = json_data['box']
    text = json_data['text']
    font_size, text_lst = get_text_and_size(box, text)

    # draw text and border
    colors = {}
    colors['text_color'] = text['text_color']
    colors['border_color'] = text['border_color']
    ouput_img = draw_content(
        img_path, box, colors, font_size, text_lst
        )

    # output json

    return jsonify({}), HTTPStatus.OK

def download_img(url):
    '''
    Download image and return the path of the image
    '''
    img_name = os.path.basename(url)
    img_dir = current_app.config["IMAGES_DIR"]
    abs_path = os.path.join(img_dir, img_name)
    with open(abs_path, 'wb') as img:
        response = requests.get(url, stream=True)
        if not response.ok:
            print('Unable to get image')

        for block in response.iter_content(1024):
            if not block: break
            img.write(block)
    return abs_path

def get_text_and_size(box, text):
    '''
    return a dictionary contains font size and list of splited text
    {font_size: 5, text:[['hello', 'world'] ,['second']]}
    '''
    img_dir = current_app.config["IMAGES_DIR"]
    font_name = os.path.join(img_dir, 'test.ttf') # test font
    font_size = 10
    font = ImageFont.truetype(font_name, font_size)
    
    text_group = []
    new_group = []
    text_lst = text['content'].split()
    while text_lst:
        new_group.append(text_lst.pop(0))
        if len(new_group) == 3:
            text_group.append(new_group)
            new_group = []

    # print(text_group)

    return (font_size, text_group)

def draw_content(image_path, box, colors, font_size, text_lst):
    with Image.open(image_path) as img:
        draw = ImageDraw.Draw(img)

        # draw rectangle
        shape = [
            (box['x'], box['y']), 
            (box['x']+box['width'], box['y']+box['height'])
        ]
        draw.rectangle(shape, fill=None, outline=colors['border_color'])

        # draw text
        font = ImageFont.truetype("arial.ttf", font_size)
        draw.multiline_text(
            (box['x'], box['y']), 
            ' '.join(text_lst[0]), 
            font=font, 
            fill=colors['text_color']
            )

        img.show()
        # im.save(sys.stdout, "PNG")


