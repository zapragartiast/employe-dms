from flask import request, make_response, jsonify
from flask.views import MethodView
from src.app import db
from src.models.pegawai import Pegawai


class RegisterAPI(MethodView):
    """
    Pegawai registration
    """
    def post(self):
        post_data = request.get_json()
        pegawai = Pegawai.query.filter_by(nip=post_data.get('nip')).first()
        if not pegawai:
            try:
                pegawai = Pegawai(
                    nip=post_data.get('nip'),
                    nama=post_data.get('nama'),
                    aktif_status=post_data.get('aktif_status')
                )
                db.session.add(pegawai)
                db.session.commit()
                auth_token = pegawai.encode_auth_token(pegawai.id)
                response_object = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                    'auth_token': auth_token.decode()
                }
                return make_response(jsonify(response_object)), 201
            except Exception as e:
                response_object = {
                    'status': 'fail',
                    'message': 'Some error occurred. Please try again.'
                }
                return make_response(jsonify(response_object)), 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'User with the NIP already exist. Please login.'
            }
            return make_response(jsonify(response_object)), 202


registration_view = RegisterAPI.as_view('register_api')
