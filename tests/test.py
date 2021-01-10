import os, sys

sys.path.append('..')
from app.controllers.image import get_text_and_size

JSON_DATA = {
    "font_url": "https://storage.googleapis.com/dipp-massimo-development-fonts/4f2cf2b6b99d96ca.ttf",
    "image_url": "https://storage.googleapis.com/dipp-massimo-development-images/1f1282fef735f349.jpg",
    "text": {
        "content": "Dipp inc, thinking out of how to draw a text on the box.",
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

    def test_get_text_and_size(self):
        font_path = os.path.join(
            os.getcwd(),
            '..',
            'fonts',
            'test.ttf'
            )
        ret = get_text_and_size(
            self.json_data['box'],
            self.json_data['text'],
            font_path
        )

        print(ret)

if __name__ == '__main__':
    t = TestCase()
    t.test_get_text_and_size()