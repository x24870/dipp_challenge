from http import HTTPStatus
from flask import jsonify

class APIResponse():
    def success(json_resp):
        return jsonify(json_resp), HTTPStatus.OK

    def not_found():
        json_resp = {
            'code': 404,
            'message': 'Nothing matches the given URI'
        }
        return jsonify(json_resp), HTTPStatus.NOT_FOUND

    def method_not_allowed():
        json_resp = {
            'code': 405,
            'message': 'Nothing matches the given URI'
        }
        return jsonify(json_resp), HTTPStatus.METHOD_NOT_ALLOWED

    def invalid_params():
        json_resp = {
            'code': 400,
            'message': 'Please inspect your params or query valid'
        }
        return jsonify(json_resp), HTTPStatus.BAD_REQUEST

    def unable_fetch_file():
        json_resp = {
            'code': 400,
            'message': "Can not get file's data from url"
        }
        return jsonify(json_resp), HTTPStatus.BAD_REQUEST

    def unable_fit_content():
        json_resp = {
            'code': 400,
            'message': "Can not make a text fit in a box"
        }
        return jsonify(json_resp), HTTPStatus.BAD_REQUEST