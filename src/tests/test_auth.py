import unittest
import json
import io
import time

from src.app import db
from src.models.pegawai import Pegawai, BlackListToken
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

    def test_user_status(self):
        data_load = {
            'nip': '100000000000000012',
            'nama': 'John Wick',
            'aktif_status': '1',
        }
        data_load = {key: str(value) for key, value in data_load.items()}
        data_load['avatar'] = (io.BytesIO(b'test'), 'src/tests/dadang.jpg')
        with self.client:
            register_response = self.client.post(
                '/pegawai/auth/register',
                data=data_load,
                content_type='multipart/form-data'
            )
            response = self.client.get(
                '/pegawai/auth/status',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        register_response.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['data'] is not None)
            self.assertTrue(data['data']['nip'] == '100000000000000012')
            self.assertEqual(response.status_code, 200)

    def test_non_registered_user_login(self):
        data = {
            'nip': '100000000000000010'
        }
        with self.client:
            response = self.client.post(
                '/pegawai/auth/login',
                data=data,
                content_type='multipart/form-data'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'User does not exists')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 404)

    def test_valid_logout(self):
        data = {
            'nip': '100000000000000012',
            'nama': 'John Wick',
            'aktif_status': '1',
        }
        data = {key: str(value) for key, value in data.items()}
        data['avatar'] = (io.BytesIO(b'test'), 'src/tests/dadang.jpg')
        with self.client:
            # user register
            resp_register = self.client.post(
                '/pegawai/auth/register',
                data=data,
                content_type='multipart/form-data'
            )
            data_register = json.loads(resp_register.data.decode())
            self.assertTrue(data_register['status'] == 'success')
            self.assertTrue(data_register['message'] == 'Successfully registered.')
            self.assertTrue(data_register['auth_token'])
            self.assertTrue(resp_register.content_type == 'application/json')
            self.assertEqual(resp_register.status_code, 201)
            # user login
            resp_login = self.client.post(
                '/pegawai/auth/login',
                data={
                    'nip': '100000000000000012'
                },
                content_type='multipart/form-data'
            )
            data_login = json.loads(resp_login.data.decode())
            self.assertTrue(data_login['status'] == 'success')
            self.assertTrue(data_login['message'] == 'Successfully login.')
            self.assertTrue(data_login['auth_token'])
            self.assertTrue(resp_login.content_type == 'application/json')
            self.assertEqual(resp_login.status_code, 200)
            # valid token logout
            response = self.client.post(
                '/pegawai/auth/logout',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logout')
            self.assertEqual(response.status_code, 200)

    def test_invalid_logout(self):
        data = {
            'nip': '100000000000000012',
            'nama': 'John Wick',
            'aktif_status': '1',
        }
        data = {key: str(value) for key, value in data.items()}
        data['avatar'] = (io.BytesIO(b'test'), 'src/tests/dadang.jpg')
        with self.client:
            # user registration
            resp_register = self.client.post(
                '/pegawai/auth/register',
                data=data,
                content_type='multipart/form-data'
            )
            data_register = json.loads(resp_register.data.decode())
            self.assertTrue(data_register['status'] == 'success')
            self.assertTrue(data_register['message'] == 'Successfully registered.')
            self.assertTrue(data_register['auth_token'])
            self.assertTrue(resp_register.content_type == 'application/json')
            self.assertEqual(resp_register.status_code, 201)
            # user login
            resp_login = self.client.post(
                '/pegawai/auth/login',
                data={
                    'nip': '100000000000000012'
                },
                content_type='multipart/form-data'
            )
            data_login = json.loads(resp_login.data.decode())
            self.assertTrue(data_login['status'] == 'success')
            self.assertTrue(data_login['message'] == 'Successfully login.')
            self.assertTrue(data_login['auth_token'])
            self.assertTrue(resp_login.content_type == 'application/json')
            self.assertEqual(resp_login.status_code, 200)
            # invalid token logout
            time.sleep(3)
            response = self.client.post(
                '/pegawai/auth/logout',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Signature expired. Please login again.')
            self.assertEqual(response.status_code, 401)

    def test_valid_blacklisted_token_logout(self):
        data = {
            'nip': '100000000000000012',
            'nama': 'John Wick',
            'aktif_status': '1'
        }
        data = {key: str(value) for key, value in data.items()}
        data['avatar'] = (io.BytesIO(b'test'), 'src/tests/dadang.jpg')
        with self.client:
            # user registration
            resp_register = self.client.post(
                '/pegawai/auth/register',
                data=data,
                content_type='multipart/form-data'
            )
            data_register = json.loads(resp_register.data.decode())
            self.assertTrue(data_register['status'] == 'success')
            self.assertTrue(data_register['message'] == 'Successfully registered.')
            self.assertTrue(data_register['auth_token'])
            self.assertTrue(resp_register.content_type == 'application/json')
            self.assertEqual(resp_register.status_code, 201)
            # user login
            resp_login = self.client.post(
                '/pegawai/auth/login',
                data={
                    'nip': '100000000000000012'
                },
                content_type='multipart/form-data'
            )
            data_login = json.loads(resp_login.data.decode())
            self.assertTrue(data_login['status'] == 'success')
            self.assertTrue(data_login['message'] == 'Successfully login.')
            self.assertTrue(data_login['auth_token'])
            self.assertTrue(resp_login.content_type == 'application/json')
            self.assertEqual(resp_login.status_code, 200)
            # validate blacklist
            blacklist_token = BlackListToken(
                token=json.loads(resp_login.data.decode())['auth_token']
            )
            db.session.add(blacklist_token)
            db.session.commit()
            response = self.client.post(
                '/pegawai/auth/logout',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Token blacklisted. Please login again.')
            self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
