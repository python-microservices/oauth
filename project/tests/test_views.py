import json
import os
import unittest
from typing import Dict, List, Union, Text

from project import create_app
from project.models.models import User, db

def _format_response(response: Text = "") -> Union[List, Dict]:
    return json.loads(response)


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        os.environ["ENVIRONMENT"] = "test"
        self.app, self.db = create_app()
        self.base_url = self.app.config["APPLICATION_ROOT"]
        self.client = self.app.test_client()

    def tearDown(self):
        os.unlink(self.app.config['DATABASE'])

    def _create_user(self, username, password):
        with self.app.test_request_context():
            user = User(
                username=username,
                password=password
            )
            # insert the user
            db.session.add(user)
            db.session.commit()
            return user.id

    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 404)

    def test_protected_view_error(self):
        response = self.client.get('{base_url}/check-token'.format(base_url=self.base_url))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(_format_response(response.data)["description"], "Request does not contain an access token")
        self.assertEqual(_format_response(response.data)["error"], "Authorization Required")

    def test_login_error(self):
        response = self.client.post('{base_url}/login'.format(base_url=self.base_url),
                                    data={"username": "", "password": ""})
        self.assertEqual(response.status_code, 401)
        self.assertEqual(_format_response(response.data)["message"], 'Bad username and/or password')

    def test_login_ok(self):
        username = "test"
        password = "1234"
        self._create_user(username, password)
        response = self.client.post('{base_url}/login'.format(base_url=self.base_url),
                                    data={"username": username, "password": password})
        self.assertEqual(response.status_code, 200)
        result = _format_response(response.data)["access_token"]
        self.assertGreater(len(result), 0)

        # check protected
        response = self.client.get('{base_url}/check-token'.format(base_url=self.base_url),
                                   headers={'authorization': 'JWT {}'.format(result)})
        self.assertEqual(response.status_code, 200)
