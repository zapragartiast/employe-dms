import unittest

from src.app import db
from src.models.pegawai import Pegawai
from src.tests.base import BaseTestCase


class TestPegawaiModel(BaseTestCase):
    def test_encode_auth_token(self):
        pegawai = Pegawai(
            nip='100000000000000012',
            nama="John Wick",
            aktif_status='1',
            avatar=''
        )
        db.session.add(pegawai)
        db.session.commit()
        auth_token = pegawai.encode_auth_token(pegawai.id)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        pegawai = Pegawai(
            nip='100000000000000012',
            nama="John Wick",
            aktif_status='1',
            avatar=''
        )
        db.session.add(pegawai)
        db.session.commit()
        auth_token = pegawai.encode_auth_token(pegawai.id)
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertTrue(Pegawai.decode_auth_token(auth_token.decode("utf-8")) == 1)


if __name__ == '__main__':
    unittest.main()
