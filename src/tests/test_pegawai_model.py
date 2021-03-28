import unittest

from src.app import db
from src.models.pegawai import Pegawai
from src.tests.base import BaseTestCase


class TestPegawaiModel(BaseTestCase):
    def test_encode_auth_token(self):
        pegawai = Pegawai(
            nip=149202920102392,
            email='zapra@me.com',
            password='123456',
        )
        db.session.add(pegawai)
        db.session.commit()
        auth_token = pegawai.encode_auth_token(pegawai.id)
        self.assertTrue(isinstance(auth_token, bytes))


if __name__ == '__main__':
    unittest.main()
