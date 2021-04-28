from flask import request, make_response, jsonify
from flask.views import MethodView
from src.models.pegawai import Pegawai


class DetailPegawai(MethodView):
    def get(self, id):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = Pegawai.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                pegawai = Pegawai.query.filter_by(id=id).first()
                if pegawai:
                    if pegawai.avatar == '':
                        pegawai.avatar = 'Can aya foto na euy'
                    else:
                        pegawai.avatar = request.url_root + 'files/' + pegawai.avatar
                    response_object = {
                        'status': 'success',
                        'message': 'Keterangan pegawai',
                        'data': {
                            'id': pegawai.id,
                            'nip': str(pegawai.nip),
                            'nik': str(pegawai.nik),
                            'gelar_depan': pegawai.gelar_depan,
                            'gelar_belakang': pegawai.gelar_belakang,
                            'nama': pegawai.nama,
                            'avatar': pegawai.avatar,
                            'aktif_status': str(pegawai.aktif_status)
                        }
                    }
                    return make_response(jsonify(response_object)), 200
                else:
                    response_object = {
                        'status': 'fail',
                        'message': 'Pegawai tidak ditemukan'
                    }
                    return make_response(jsonify(response_object)), 404
            else:
                response_object = {
                    'status': 'fail',
                    'message': resp
                }
                return make_response(jsonify(response_object)), 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'Please provide valid auth token'
            }
            return make_response(jsonify(response_object)), 401


detail_pegawai = DetailPegawai.as_view('detail_pegawai')
