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
        avatar = request.files['avatar']
        pegawai = Pegawai.query.filter_by(nip=request.form.get('nip')).first()
        if not pegawai:
            try:
                pegawai = Pegawai(
                    nip=request.form.get('nip'),
                    nik=request.form.get('nik'),
                    gelar_depan=request.form.get('gelar_depan'),
                    gelar_belakang=request.form.get('gelar_belakang'),
                    nama=request.form.get('nama'),
                    avatar=avatar.filename,
                    tempat_lahir=request.form.get('tempat_lahir'),
                    tanggal_lahir=request.form.get('tanggal_lahir'),
                    jenis_kelamin=request.form.get('jenis_kelamin'),
                    aktif_status=request.form.get('aktif_status')
                )
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
                        'message': 'Please upload png, jpg, jpeg file extensions'
                    }
                    return make_response(jsonify(response_object)), 400
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


class LoginAPI(MethodView):
    """
    Pegawai login
    """
    def post(self):
        post_data = request.form.get
        try:
            pegawai = Pegawai.query.filter_by(
                nip=post_data('nip')
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
