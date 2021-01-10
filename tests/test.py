import os, sys

sys.path.append('..')
from app.controllers.image import get_text_and_size, draw_content

JSON_DATA = {
    "font_url": "https://storage.googleapis.com/dipp-massimo-development-fonts/4f2cf2b6b99d96ca.ttf",
    "image_url": "https://storage.googleapis.com/dipp-massimo-development-images/1f1282fef735f349.jpg",
    "text": {
        "content": "Dipp inc, thinking out of how to draw a text on the box. asdw5 asdqq asdsas48956d qwghkad522p",
        "text_color": "#000000",
        "border_color": "#000000"
    },
    "box": {
        "x": 40,
        "y": 100,
        "width": 500,
        "height": 180
    }
}

class TestCase():
    def __init__(self):
        self.json_data = JSON_DATA
        self.img_path = os.path.join(
            os.path.dirname(os.getcwd()),
            'images',
            'test.jpg'
        )
        self.font_path = os.path.join(
            os.getcwd(),
            '..',
            'fonts',
            'test.ttf'
            )

    def test_get_text_and_size(self):
        font_size, newline_idx = get_text_and_size(
            self.json_data['box'],
            self.json_data['text'],
            self.font_path
        )

        print(font_size, newline_idx)
        return font_size, newline_idx

    def test_draw_content(self):
        font_size, newline_idx = self.test_get_text_and_size()
        ouput_img = draw_content(
            self.img_path, 
            self.font_path, 
            self.json_data['box'], 
            self.json_data['text'], 
            font_size, 
            newline_idx
        )

if __name__ == '__main__':
    t = TestCase()
    t.test_draw_content()