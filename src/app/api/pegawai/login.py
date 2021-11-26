from flask import request, make_response, jsonify
from flask.views import MethodView
from src.models.pegawai import Pegawai


class LoginAPI(MethodView):
    """Pegawai Login"""
    def post(self):
        post_data = request.form.get
        try:
            pegawai = Pegawai.query.filter_by(
                nip=post_data('nip'),
                nik=post_data('nik')
            ).first()
            if pegawai:
                auth_token = pegawai.encode_auth_token(pegawai.id)
                if auth_token:
                    response_object = {
                        'status': 'success',
                        'message': 'Berhasil login.',
                        'auth_token': auth_token.decode()
                    }
                    return make_response(jsonify(response_object)), 200
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'Pengguna tidak ditemukan.'
                }
                return make_response(jsonify(response_object)), 404
        except Exception as e:
            response_object = {
                'status': 'fail',
                'message': 'Try again',
                'error': e
            }
            return make_response(jsonify(response_object)), 500


login_view = LoginAPI.as_view('login_api')
