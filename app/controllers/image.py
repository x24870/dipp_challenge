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

    # generate response json
    box = json_data['box']
    text = json_data['text']
    json_resp = gen_resp_json(img_path, font_path, box, text)

    # draw text and border
    colors = (text['border_color'], text['text_color'])
    draw_content(img_path, font_path, box, colors, json_resp)
    
    return jsonify(json_resp), HTTPStatus.OK

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
    # MIN 1 pixel, MAX 4K pixel
    l = 1
    r = 4096
    last_fit = None
    while l < r:
        font_size = (r - l) // 2 + l
        font = ImageFont.truetype(font_path, font_size)
        print(f'l: {l}  r: {r}  font:{font_size}')

        words = text_lst[:]
        splits = []
        init_splite = {
            'content': '',
            'font_size': font_size,
            'x': box['x'],
            'y': box['y']
        }
        new_splite = None
        cur_h = cur_w = 0 # inbox coordinate
        new_line = True
        fit_content = False
        while words:
            word = words[0] + ' '
            word_size = get_text_dimensions(word, font)

            # if this word is the first word of line
            # record the index of the word
            if new_line:
                new_splite = init_splite.copy()
                new_splite['y'] += cur_h
                cur_h += word_size[1]
                splits.append(new_splite)
                new_line = False
                if cur_h > box['height']:
                    splits.clear()
                    fit_content = False
                    break
            
            # left space can't accommodate this word
            # move to next line
            cur_w += word_size[0]
            if cur_w > box['width']:
                cur_w = 0
                new_line = True
            else:
                new_splite['content'] += word
                words.pop(0)
                if not words: fit_content = True
            
        # if current size can fit box
        # store current result and increse font size
        if fit_content:
            last_fit = splits
            l = font_size + 1
        else:
            r = font_size

    return last_fit

def draw_content(img_path, font_path, box, colors, json_resp):
    with Image.open(img_path) as img:
        draw = ImageDraw.Draw(img)

        # draw rectangle
        shape = [
            (box['x'], box['y']), 
            (box['x']+box['width'], box['y']+box['height'])
        ]
        draw.rectangle(shape, fill=None, outline=colors[0])

        # draw text
        font_size = json_resp['splits'][0]['font_size']
        font = ImageFont.truetype(font_path, font_size)
        for s in json_resp['splits']:
            draw.multiline_text(
                (s['x'], s['y']), 
                s['content'], 
                font=font, 
                fill=colors[1]
                )

        # img.show()
        img.save(json_resp['resource'])
    

def gen_resp_json(image_path, font_path, box, text):
    json_resp = {}
    # resource
    resource = os.path.basename(image_path)
    resource = image_path.split('.')
    resource = f'{resource[0]}_output.{resource[1]}'
    resource = os.path.join('D:\projects\dipp_challenge\dipp_challenge\images', resource)
    json_resp['resource'] = resource

    json_resp['splits'] = get_text_and_size(
        box, text, font_path
    )

    print(json_resp)
    return json_resp

def get_text_dimensions(text_string, font):
    # https://stackoverflow.com/a/46220683/9263761
    ascent, descent = font.getmetrics()

    text_width = (
        font.getmask(text_string).getbbox()[2]
        + font.getlength(' ')
    )
    text_height = font.getmask(text_string).getbbox()[3] + descent

    return (text_width, text_height)