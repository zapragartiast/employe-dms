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
    avatar = db.Column(db.Text)
    tempat_lahir = db.Column(db.String(255))
    tanggal_lahir = db.Column(db.Date)
    jenis_kelamin = db.Column(db.SmallInteger)
    aktif_status = db.Column(db.SmallInteger, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    def __init__(
            self,
            nip,
            nama,
            aktif_status,
            nik=None,
            gelar_depan=None,
            gelar_belakang=None,
            avatar=None,
            tempat_lahir=None,
            tanggal_lahir=None,
            jenis_kelamin=None,
    ):
        self.nip = nip
        self.nik = nik
        self.gelar_depan = gelar_depan
        self.gelar_belakang = gelar_belakang
        self.nama = nama
        self.avatar = avatar
        self.tempat_lahir = tempat_lahir
        self.tanggal_lahir = tanggal_lahir
        self.jenis_kelamin = jenis_kelamin
        self.aktif_status = aktif_status
        self.created_at = datetime.datetime.utcnow()
        self.updated_at = datetime.datetime.utcnow()

    def encode_auth_token(self, pegawai_id):
        """
        Generates auth token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=float(app.config['JWT_TTL'])),
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
            is_blacklisted_token = BlackListToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please login again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please login again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please login again.'


class BlackListToken(db.Model):
    """
    Token Model for storing JWT Tokens
    """
    __tablename__ = 'blacklist_token'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.Text, unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    @staticmethod
    def check_blacklist(auth_token):
        res = BlackListToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False