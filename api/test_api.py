from rest_framework import status
import unittest
import requests


class TestBasic(unittest.TestCase):

    def setUp(self):
        self.login_url = 'http://127.0.0.1:8000/api/obtain_token/'
        self.add_user_url = 'http://127.0.0.1:8000/api/signup/'
        self.credentials = {
            "username": "admin@admin.com",
            "password": "admin740",
        }
        response = requests.post(url=self.login_url, json=self.credentials)
        response = response.json()
        self.token = response["token"]

    def test_obtain_token(self):
        response = requests.post(url=self.login_url, json=self.credentials)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_obtain_token_negaive(self):
        cases = [({
                      "username": "",
                      "password": "",
                  },
                  {
                      "username": ["This field may not be blank."],
                      "password": ["This field may not be blank."]
                  }),
            ({
                 "username": "admin",
                 "password": "123",

             },
             {
                 "non_field_errors": [
                     "Unable to log in with provided credentials."
                 ]
             }
            ),
            ({"username": "admin@gmail.com",
              "password": "123jwueibeuf"},
             {
                 "non_field_errors": [
                     "Unable to log in with provided credentials."
                 ]
             }
             ),
        ]

        for сredentials, expected in cases:
            with self.subTest():
                response = requests.post(url=self.login_url, json=сredentials)
                response = response.json()
                self.assertEqual(response, expected)

    def test_add_user_negative(self):
        cases = [
            (self.token,
             {
                 "username": "",
                 "password": "",
                 "balance": "",
                 "currency": "",
             },
             {"username": ["This field may not be blank."],
              "password": ["This field may not be blank."],
              "balance": ["A valid number is required."],
              "currency": ["This field may not be null."]}),

            (self.token,
             {
                 "username": "user",
                 "password": "123",
                 "balance": "100000000.333",
                 "currency": "dollar",
             },
             {
                 "username": [
                     "Enter a valid email address."
                 ],
                 "password": ["Ensure this field has at least 8 characters."],
                 "balance": ["Ensure that there are no more than 8 digits in total."],
                 "currency": ["Object with short_name=dollar does not exist."]
             }
             ), ('123456',
                 {"username": "user@gmail.com",
                  "password": "WFWdc213$&ZZv12",
                  "balance": "100",
                  "currency": "USD", },
                 {
                     "detail": "Invalid token."
                 }
                 )
        ]

        for token, data, expected in cases:
            with self.subTest():
                header = {'Authorization': f'Token {token}'}
                response = requests.post(url=self.add_user_url, headers=header, json=data)
                response = response.json()
                self.assertEqual(response, expected)
