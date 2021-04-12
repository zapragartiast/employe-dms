import os

from flask import request, make_response, jsonify
from flask.views import MethodView
from src.app import db, app
from src.models.pegawai import Pegawai, BlackListToken
from werkzeug.utils import secure_filename


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


class RegisterAPI(MethodView):
    """
    Pegawai registration
    """
    def post(self):
        post_data = request.form.get
        pegawai = Pegawai.query.filter_by(
            nip=post_data('nip'),
            nik=post_data('nik')
        ).first()
        if not pegawai:
            try:
                avatar = request.files['avatar']
                pegawai = Pegawai(
                    nip=post_data('nip'),
                    nama=str.upper(post_data('nama')),
                    aktif_status=post_data('aktif_status'),
                    nik=post_data('nik'),
                    avatar=avatar.filename,
                    gelar_depan=post_data('gelar_depan'),
                    gelar_belakang=post_data('gelar_belakang'),
                    tempat_lahir=post_data('tempat_lahir'),
                    tanggal_lahir=post_data('tanggal_lahir'),
                    jenis_kelamin=post_data('jennies_kelamin')
                )

                if pegawai.avatar == '':
                    db.session.add(pegawai)
                    db.session.commit()
                    auth_token = pegawai.encode_auth_token(pegawai.id)
                    response_object = {
                        'status': 'success',
                        'message': 'Successfully registered.',
                        'auth_token': auth_token.decode()
                    }
                    return make_response(jsonify(response_object)), 201
                
                if avatar and allowed_file(avatar.filename):
                    filename = secure_filename(avatar.filename)
                    avatar.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    db.session.add(pegawai)
                    db.session.commit()
                    auth_token = pegawai.encode_auth_token(pegawai.id)
                    response_object = {
                        'status': 'success',
                        'message': 'Successfully registered.',
                        'auth_token': auth_token.decode()
                    }
                    return make_response(jsonify(response_object)), 201
                else:
                    response_object = {
                        'status': 'fail',
                        'message': 'Something error when uploading your files.'
                    }
                    make_response(jsonify(response_object)), 401

            except Exception as e:
                response_object = {
                    'status': 'fail',
                    'message': 'An error occurred. Please try again.'
                }
                return make_response(jsonify(response_object)), 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'User with the NIP already exist. Please login.'
            }
            return make_response(jsonify(response_object)), 202


class LoginAPI(MethodView):
    """
    Pegawai login
    """
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
                        'message': 'Successfully login.',
                        'auth_token': auth_token.decode()
                    }
                    return make_response(jsonify(response_object)), 200
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'User does not exists'
                }
                return make_response(jsonify(response_object)), 404
        except Exception as e:
            print(e)
            response_object = {
                'status': 'fail',
                'message': 'Try again'
            }
            return make_response(jsonify(response_object)), 500


class PegawaiAPI(MethodView):
    """
    Pegawai Resources
    """
    def get(self):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = Pegawai.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                pegawai = Pegawai.query.filter_by(id=resp).first()
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
                        'nama': pegawai.nama,
                        'nik': str(pegawai.nik),
                        'aktif_status': str(pegawai.aktif_status),
                        'avatar': pegawai.avatar
                    }
                }
                return make_response(jsonify(response_object)), 200
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


class UpdatePegawai(MethodView):
    def put(self):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            try:
                response_object = {
                    'status': 'success',
                    'id': 'ok'
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
                'message': 'Access restricted. Please provide valid auth token'
            }
            return make_response(jsonify(response_object)), 401


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


registration_view = RegisterAPI.as_view('register_api')
login_view = LoginAPI.as_view('login_api')
pegawai_api = PegawaiAPI.as_view('pegawai_api')
logout_view = LogoutAPI.as_view('logout_api')
detail_pegawai = DetailPegawai.as_view('detail_pegawai')
update_pegawai = UpdatePegawai.as_view('update_pegawai')
