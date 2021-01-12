import unittest
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

    def test_invalid_http_method(self):
        resp = self.api_draw_request('GET', JSON_DATA)
        self.assertEqual(resp.status_code, 405)
        resp = self.api_draw_request('PUT', JSON_DATA)
        self.assertEqual(resp.status_code, 405)
        resp = self.api_draw_request('DELETE', JSON_DATA)
        self.assertEqual(resp.status_code, 405)

if __name__ == '__main__':
    unittest.main()