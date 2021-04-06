import unittest
import json
import io

from src.app import db
from src.models.pegawai import Pegawai
from src.tests.base import BaseTestCase


class TestAuthBluePrint(BaseTestCase):
    def test_registration(self):
        data = {
            'nip': '100000000000000012',
            'nama': 'John Wick',
            'aktif_status': '1',
        }
        data = {key: str(value) for key, value in data.items()}
        data['avatar'] = (io.BytesIO(b'test'), 'src/tests/dadang.jpg')
        with self.client:
            response = self.client.post(
                '/pegawai/auth/register',
                data=data,
                content_type='multipart/form-data'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully registered.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_registration_with_already_registered_user(self):
        pegawai = Pegawai(
            nip='100000000000000012',
            nama='John Wick',
            aktif_status='1'
        )
        data = {
            'nip': '100000000000000012',
            'nama': 'John Wick',
            'aktif_status': '1',
        }
        data = {key: str(value) for key, value in data.items()}
        data['avatar'] = (io.BytesIO(b'test'), 'src/tests/dadang.jpg')
        db.session.add(pegawai)
        db.session.commit()
        with self.client:
            response = self.client.post(
                '/pegawai/auth/register',
                data=data,
                content_type='multipart/form-data'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(
                data['message'] == 'User with the NIP already exist. Please login.'
            )
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 202)

    def test_registered_user_login(self):
        data = {
            'nip': '100000000000000012',
            'nama': 'John Wick',
            'aktif_status': '1',
        }
        data = {key: str(value) for key, value in data.items()}
        data['avatar'] = (io.BytesIO(b'test'), 'src/tests/dadang.jpg')
        with self.client:
            # pegawai registration
            resp_register = self.client.post(
                '/pegawai/auth/register',
                data=data,
                content_type='multipart/form-data',
            )
            data_register = json.loads(resp_register.data.decode())
            self.assertTrue(data_register['status'] == 'success')
            self.assertTrue(
                data_register['message'] == 'Successfully registered.'
            )
            self.assertTrue(data_register['auth_token'])
            self.assertTrue(resp_register.content_type == 'application/json')
            self.assertEqual(resp_register.status_code, 201)
            # registered user login
            response = self.client.post(
                '/pegawai/auth/login',
                data={
                    'nip': '100000000000000012'
                },
                content_type='multipart/form-data'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully login.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
