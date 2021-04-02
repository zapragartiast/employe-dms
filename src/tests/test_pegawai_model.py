import unittest

from src.app import db
from src.models.pegawai import Pegawai
from src.tests.base import BaseTestCase


class TestPegawaiModel(BaseTestCase):
    def test_encode_decode_auth_token(self):
        pegawai = Pegawai(
            nip='100000000000000012',
            nik='12345678',
            gelar_depan='',
            gelar_belakang='',
            nama="Zefri Kurnia Salman",
            avatar='',
            tempat_lahir='',
            tanggal_lahir='02-28-1990',
            jenis_kelamin='2',
            aktif_status='1'
        )
        db.session.add(pegawai)
        db.session.commit()
        auth_token = pegawai.encode_auth_token(pegawai.id)
        self.assertTrue(Pegawai.decode_auth_token(auth_token) == 1)


if __name__ == '__main__':
    unittest.main()
