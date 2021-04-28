import datetime

from flask import request, make_response, jsonify
from flask.views import MethodView
from src.app import db
from src.models.pegawai import Pegawai


class UpdatePegawai(MethodView):
    def put(self):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = Pegawai.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                pegawai = Pegawai.query.filter_by(id=resp).first()
                if pegawai:
                    try:
                        pegawai.nama = str.upper(request.form.get('nama'))
                        pegawai.nik = request.form.get('nik')
                        pegawai.updated_at = datetime.datetime.now()
                        db.session.commit()
                        response_object = {
                            'status': 'success',
                            'message': 'Pegawai has been updated',
                            'data': {
                                'nama': pegawai.nama
                            }
                        }
                        return make_response(jsonify(response_object)), 200
                    except Exception as e:
                        response_object = {
                            'status': 'fail',
                            'message': e
                        }
                        return make_response(jsonify(response_object)), 401
                else:
                    response_object = {
                        'status': 'fail',
                        'message': 'Fatal error'
                    }
                    return make_response(jsonify(response_object)), 500
            else:
                response_object = {
                    'status': 'fail',
                    'message': resp
                }
                return make_response(jsonify(response_object)), 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'Access restricted. Please provide valid auth token'
            }
            return make_response(jsonify(response_object)), 401


update_pegawai = UpdatePegawai.as_view('update_pegawai')
