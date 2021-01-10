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
    img_path = download_img(json_data['image_url'])

    #download font
    font_path = download_font(json_data['font_url'])

    # calculate font size and split text
    box = json_data['box']
    text = json_data['text']
    font_size, text_lst = get_text_and_size(box, text, font_path)

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

def download_font(url):
    '''
    Download font and return the path of the font
    '''
    font_name = os.path.basename(url)
    font_dir = current_app.config["FONTS_DIR"]
    abs_path = os.path.join(font_dir, font_name)
    with open(abs_path, 'wb') as font:
        response = requests.get(url, stream=True)
        if not response.ok:
            print('Unable to get font')

        for block in response.iter_content(1024):
            if not block: break
            font.write(block)
    return abs_path

def get_text_and_size(box, text, font_path):
    '''
    return a dictionary contains font size and index of word of new line
    {font_size: 8, newline_idx:[0, 3, 9]}
    '''
    text_lst = text['content'].split()
    newline_idx = []
    origin_len = len(text_lst)
    # min 1 pixel, max 4K pixel
    l = MIN_SIZE = 1
    r = MAX_SIZE = 4096
    while l < r:
        font_size = (r - l) // 2 + l
        font = ImageFont.truetype(font_path, font_size)

        words = text_lst[:]
        newline_idx = []
        cur_h = cur_w = 0
        new_line = True
        fit_content = False
        while words:
            word = words[0]
            word_size = font.getsize(word)

            # if this word is the first word of line
            # record the index of the word
            if new_line:
                cur_h += word_size[1]
                idx = origin_len - len(words)
                newline_idx.append(idx)
                new_line = False
                if cur_h > box['height']: break
            
            cur_w += word_size[0]
            # left space can't accommodate this word
            # move to next line
            if cur_w > box['width']:
                cur_w = 0
                new_line = True
            else:
                words.pop(0)
        else:
            fit_content = True

        # if current size can fit box
        # increse font size
        if fit_content:
            l = font_size + 1
        else:
            r = font_size

    return (l, newline_idx)

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


