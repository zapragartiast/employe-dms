from flask import request, make_response, jsonify
from flask.views import MethodView
from src.models.pegawai import Pegawai, BlackListToken
from src.app import db


class LogoutAPI(MethodView):
    def post(self):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = Pegawai.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                blacklist_token = BlackListToken(token=auth_token)
                try:
                    db.session.add(blacklist_token)
                    db.session.commit()
                    response_object = {
                        'status': 'success',
                        'message': 'Successfully logout'
                    }
                    return make_response(jsonify(response_object)), 200
                except Exception as e:
                    response_object = {
                        'status': 'fail',
                        'message': e
                    }
                    return make_response(jsonify(response_object)), 200
            else:
                response_object = {
                    'status': 'fail',
                    'message': resp
                }
                return make_response(jsonify(response_object)), 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide valid auth token'
            }
            return make_response(jsonify(response_object)), 403


logout_view = LogoutAPI.as_view('logout_api')
