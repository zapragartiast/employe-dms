import unittest
import json

from src.app import db
from src.models.pegawai import Pegawai
from src.tests.base import BaseTestCase


class TestAuthBluePrint(BaseTestCase):
    """Test for user registration"""
    def test_registration(self):
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps(dict(
                    nip='100000000000000012',
                    nama='Zefri Kurnia Salman',
                    aktif_status='1'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully registered.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_registration_with_alrady_registered_user(self):
        """Test registration with already registered NIP"""
        pegawai = Pegawai(
            nip='100000000000000012',
            nama='Zefri Kurnia Salman',
            aktif_status='1'
        )
        db.session.add(pegawai)
        db.session.commit()
        with self.client:
            response = self.client.post(
                '/auth/register',
                data = json.dumps(dict(
                    nip='100000000000000012',
                    nama='Zefri Kurnia Salman',
                    aktif_status='1'
                )),
                content_type = 'application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(
                data['message'] == 'User with the NIP already exist. Please login.'
            )
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 202)


if __name__ == '__main__':
    unittest.main()
