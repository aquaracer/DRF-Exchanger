from rest_framework import status
import unittest
import requests
from .models import AdvUser
import Exchanger.secret


class TestBasic(unittest.TestCase):

    def get_json(self, **kwargs):
        response = requests.post(**kwargs)
        return response.json()

    def setUp(self):
        self.login_url = 'http://127.0.0.1:8000/api/obtain_token/'
        self.add_user_url = 'http://127.0.0.1:8000/api/signup/'
        self.transfers_url = 'http://127.0.0.1:8000/api/'
        self.credentials = Exchanger.secret.test_credentials
        token = self.get_json(url=self.login_url, json=self.credentials)
        self.token = token['token']

    def test_obtain_token(self):
        response = requests.post(url=self.login_url, json=self.credentials)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_obtain_token_negaive(self):
        cases = [

            ({}, {
                "username": ["This field is required."],
                "password": ["This field is required."]
            }),
            ({
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
                self.assertEqual(self.get_json(url=self.login_url, json=сredentials), expected)

    def test_add_user(self):
        data = {
            "username": "user@mail.ru",
            "password": "WFWdc213$&ZZv12xcz",
            "balance": "100.00",
            "currency": "USD"
        }
        response = requests.post(url=self.add_user_url,
                                 headers={'Authorization': f'Token {self.token}'},
                                 json=data)
        AdvUser.objects.filter(username=data['username']).delete()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

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
                 ),
            ('30f3ef8ee03290f2f8bb01186cf4db3f78c47b67',
             {"username": "user@gmail.com",
              "password": "WFWdc213$&ZZv12",
              "balance": "100",
              "currency": "USD", },
             {
                 "detail": "You do not have permission to perform this action."
             }
             )
        ]

        for token, data, expected in cases:
            with self.subTest():
                self.assertEqual(self.get_json(url=self.add_user_url,
                                               headers={'Authorization': f'Token {token}'},
                                               json=data), expected)

    def test_transfer(self):
        data = {
            'amount': 100.10,
            'counterparty_account': 'user@user.com'
        }
        response = requests.post(url=self.transfers_url,
                                 headers={'Authorization': f'Token {self.token}'},
                                 json=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_transfer_negative(self):
        cases = [
            (self.token,
             {},
             {
                 "amount": ["This field is required."],
                 "counterparty_account": ["This field is required."]
             }),
            (self.token,
             {
                 "amount": "",
                 'counterparty_account': '',
             },
             {
                 "amount": ["A valid number is required."],
                 "counterparty_account": ["This field may not be null."]
             }),
            (self.token,
             {
                 "amount": "abc",
                 'counterparty_account': 'user',
             },
             {
                 "amount": [
                     "A valid number is required."
                 ],
                 "counterparty_account": [
                     "Object with username=user does not exist."
                 ]
             }),
            (self.token,
             {
                 "amount": 100.333,
                 'counterparty_account': 'user111222@mail.ru',
             },
             {
                 "amount": [
                     "Ensure that there are no more than 2 decimal places."
                 ],
                 "counterparty_account": [
                     "Object with username=user111222@mail.ru does not exist."
                 ]
             }),
            ('',
             {
                 "amount": 100,
                 'counterparty_account': 'user@mail.ru',
             },
             {"detail": "Invalid token header. No credentials provided."}
             ),
            ('123',
             {
                 "amount": 100,
                 'counterparty_account': 'user@mail.ru',
             },
             {
                 "detail": "Invalid token."
             })]
        for token, data, expected in cases:
            with self.subTest():
                self.assertEqual(self.get_json(url=self.transfers_url,
                                               headers={'Authorization': f'Token {token}'},
                                               json=data), expected)

    def test_transactions_list(self):
        response = requests.get(url=self.transfers_url,
                                headers={'Authorization': f'Token {self.token}'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_transactions_list_negative(self):
        cases = [('', {"detail": "Invalid token header. No credentials provided."}),
                 ('123', {"detail": "Invalid token."})]
        for token, expected in cases:
            with self.subTest():
                response = requests.get(url=self.transfers_url,
                                        headers={'Authorization': f'Token {token}'})
                self.assertEqual(response.json(), expected)
