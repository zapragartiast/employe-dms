import datetime
import jwt

from src.app import app, db


class Pegawai(db.Model):
    """Model untuk generate tabel pegawai"""
    __tablename__ = 'pegawai'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    nip = db.Column(db.BigInteger, unique=True, nullable=False)
    nik = db.Column(db.BigInteger, unique=True)
    gelar_depan = db.Column(db.String(255))
    gelar_belakang = db.Column(db.String(255))
    nama = db.Column(db.String(255), nullable=False)
    tempat_lahir = db.Column(db.String(255))
    tanggal_lahir = db.Column(db.Date)
    jenis_kelamin = db.Column(db.SmallInteger)
    aktif_status = db.Column(db.SmallInteger, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, nip, nama, aktif_status):
        self.nip = nip
        self.nama = nama
        self.aktif_status = aktif_status
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()

    def encode_auth_token(self, pegawai_id):
        """
        Generates auth token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.now() + datetime.timedelta(days=365, seconds=60),
                'iat': datetime.datetime.utcnow(),
                'sub': pegawai_id
            }
            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decode auth token
        :params auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please login again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please login again.'
