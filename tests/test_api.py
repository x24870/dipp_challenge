import unittest, sys, copy
from flask import url_for
from flask_testing import TestCase
from app.app import create_app

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

JSON_DATA2 = {
    "font_url": "https://storage.googleapis.com/dipp-massimo-development-fonts/4f2cf2b6b99d96ca.ttf",
    "image_url": "https://wallpapercave.com/wp/wp2532971.jpg",
    "text": {
        "content": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.",
        "text_color": "#ffffff",
        "border_color": "#f0f0f0"
    },
    "box": {
        "x": 100,
        "y": 100,
        "width": 800,
        "height": 300
    }
}

class SettingBase(TestCase):
    def create_app(self):
        return create_app()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def api_draw_request(self, method, json):
        if method == 'GET':
            response = self.client.get(
                url_for('app.controllers.image.draw_text_box'),
                follow_redirects=True,
                json=json
                )
        elif method == 'POST':
            response = self.client.post(
                url_for('app.controllers.image.draw_text_box'),
                follow_redirects=True,
                json=json
                )
        elif method == 'PUT':
            response = self.client.put(
                url_for('app.controllers.image.draw_text_box'),
                follow_redirects=True,
                json=json
                )
        elif method == 'DELETE':
            response = self.client.delete(
                url_for('app.controllers.image.draw_text_box'),
                follow_redirects=True,
                json=json
                )
        else:
            raise BaseException('Invalid http mothod')

        return response

class TestImageAPI(SettingBase):
    def test_valid_params(self):
        resp = self.api_draw_request('POST', JSON_DATA)
        self.assertEqual(resp.status_code, 200)
        resp = self.api_draw_request('POST', JSON_DATA2)
        self.assertEqual(resp.status_code, 200)

    def test_invalid_http_method(self):
        resp = self.api_draw_request('GET', JSON_DATA)
        self.assertEqual(resp.status_code, 405)
        resp = self.api_draw_request('PUT', JSON_DATA)
        self.assertEqual(resp.status_code, 405)
        resp = self.api_draw_request('DELETE', JSON_DATA)
        self.assertEqual(resp.status_code, 405)

    def test_invalid_params(self):
        # empty content
        json = copy.deepcopy(JSON_DATA)
        json['text']['content'] = ''
        resp = self.api_draw_request('POST', json)
        self.assertEqual(resp.status_code, 400)
        # invalid image url
        json = copy.deepcopy(JSON_DATA)
        json['image_url'] = 'https://not-exist.jpg'
        resp = self.api_draw_request('POST', json)
        self.assertEqual(resp.status_code, 400)
        # invalid font url
        json = copy.deepcopy(JSON_DATA)
        json['font_url'] = 'https://not-exist.ttf'
        resp = self.api_draw_request('POST', json)
        self.assertEqual(resp.status_code, 400)
        # unable to fit content
        json = copy.deepcopy(JSON_DATA)
        json['box']['width'] = 1
        resp = self.api_draw_request('POST', json)
        self.assertEqual(resp.status_code, 400)
        # box out of image
        json = copy.deepcopy(JSON_DATA)
        json['box']['width'] = sys.maxsize
        resp = self.api_draw_request('POST', json)
        self.assertEqual(resp.status_code, 400)

if __name__ == '__main__':
    unittest.main()