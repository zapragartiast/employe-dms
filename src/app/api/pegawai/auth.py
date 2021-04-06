import os

from flask import request, make_response, jsonify
from flask.views import MethodView
from src.app import db, app
from src.models.pegawai import Pegawai
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
        avatar = request.files['avatar']
        if not pegawai:
            try:
                pegawai = Pegawai(
                    nip=post_data('nip'),
                    nama=post_data('nama'),
                    aktif_status=post_data('aktif_status'),
                    nik=post_data('nik'),
                    avatar=post_data('avatar'),
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
                    'message': 'An error occurred. Please try again.',
                    'code': print(e)
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
            auth_token = pegawai.encode_auth_token(pegawai.id)
            if auth_token:
                response_object = {
                    'status': 'success',
                    'message': 'Successfully login.',
                    'auth_token': auth_token.decode()
                }
                return make_response(jsonify(response_object)), 200
        except Exception as e:
            print(e)
            response_object = {
                'status': 'fail',
                'message': 'Try again'
            }
            return make_response(jsonify(response_object)), 500


registration_view = RegisterAPI.as_view('register_api')
login_view = LoginAPI.as_view('login_api')
