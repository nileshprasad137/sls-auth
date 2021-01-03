import os
import json
import boto3
import http.client, urllib.parse
from typing import Tuple
import urllib.parse
from src.response import return_success, return_failure


class Settings:
    AUTH0_CALLBACK_URL = os.environ.get("AUTH0_CALLBACK_URL")
    AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID")
    AUTH0_CLIENT_SECRET = os.environ.get("AUTH0_CLIENT_SECRET")
    AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
    TABLE_NAME = os.environ.get('TABLE_NAME')


class Auth0:
    conn = http.client.HTTPSConnection(Settings.AUTH0_DOMAIN)

    @classmethod
    def get_token(cls, code: str) -> dict:
        """Getting tokens
        """
        payload = {
            "grant_type": "authorization_code",
            "client_id": Settings.AUTH0_CLIENT_ID,
            "client_secret": Settings.AUTH0_CLIENT_SECRET,
            "code": code,
            "redirect_uri": Settings.AUTH0_CALLBACK_URL
        }

        headers = {
            'Content-Type': "application/x-www-form-urlencoded"
        }

        body = urllib.parse.urlencode(payload)
        cls.conn.request("POST", "/oauth/token", body, headers)

        response = cls.conn.getresponse()
        data = response.read()

        results = json.loads(data.decode("utf-8"))
        return results

    @classmethod
    def get_user_profile(cls, code: str) -> dict:
        """Getting User Profile
        """
        token = cls.get_token(code)
        if token.get('id_token') is None or token.get('access_token') is None:
            return None

        body = json.dumps({
            'id_token': token.get('id_token')
        })

        headers = {
            'Authorization': 'Bearer {}'.format(token.get('access_token')),
            'Content-Type': 'application/json'
        }

        cls.conn.request("GET", "/userinfo", body, headers)
        response = cls.conn.getresponse()
        data = response.read()
        results = json.loads(data.decode("utf-8"))
        print(results)
        return results

    @classmethod
    def get_user_profile_from_user_info(cls, tokens: dict) -> dict:
        """Getting User Profile
        """
        print("token is below")
        print(tokens)
        if tokens.get('id_token') is None and tokens.get('access_token') is None:
            return None

        body = json.dumps({
            'id_token': tokens.get('id_token')[0]
        })

        headers = {
            'Authorization': 'Bearer {}'.format(tokens.get('access_token')[0]),
            'Content-Type': 'application/json'
        }

        cls.conn.request("GET", "/userinfo", body, headers)
        response = cls.conn.getresponse()
        data = response.read()
        results = json.loads(data.decode("utf-8"))
        print(results)
        return results


class Profile:
    table = boto3.resource('dynamodb', region_name="us-east-1").Table(Settings.TABLE_NAME)
    PARTITION_KEY = 'user_profile'

    @classmethod
    def get_item(cls, sk: str) -> dict:
        response = cls.table.get_item(
            Key={
                'pk': cls.PARTITION_KEY,
                'sk': sk
            }
        )
        return response.get('Item')

    @classmethod
    def put_item(cls, sk: str, item: dict):
        item.update({
            'pk': cls.PARTITION_KEY,
            'sk': sk
        })
        try:
            cls.table.put_item(Item=item)
            return True
        except Exception as e:
            print(str(e))
            return False

    @classmethod
    def get_or_create(cls, item: dict) -> Tuple[dict, bool]:
        if item.get('sub') is None:
            return False, None
        
        profile = cls.get_item(item['sub'])
        if profile is not None:
            # TODO: Need to hide pk and sk?
            # item.pop('pk')
            # item.pop('sk')
            return profile, False
        else:
            status = cls.put_item(item['sub'], item)
            return item if status else None, status


def index(event: dict, context):
    param = event.get('queryStringParameters', None)
    if param is None or param.get('code') is None:
        msg = "Oops, Invalid Request!!!"
        # TODO: Maybe need to show some permission denied?
        return return_failure({"status": False, "msg": msg})

    user_profile = Auth0.get_user_profile(param['code'])
    print(user_profile)
    item, created = Profile.get_or_create(user_profile)
    # TODO: You will need to redirect customers to a specific url here.
    return return_success({
        "status": True, "created?": created, "data": item})

def handle_implicit_login(event: dict, context):
    # print(json.dumps(event))
    # param = event.get('queryStringParameters', None)
    body = event.get('body')
    tokens = urllib.parse.parse_qs(body)
    print(tokens)
    user_profile = Auth0.get_user_profile_from_user_info(tokens)

    # print("body --> " , body)
    # id_token = body.split("=")[1]
    # print("id_token ---> ", id_token)
    # body = json.dumps({
    #     'id_token': id_token
    # })
    #
    # headers = {
    #     'Authorization': 'Bearer {}'.format(token.get('access_token')),
    #     'Content-Type': 'application/json'
    # }
    #
    # cls.conn.request("GET", "/userinfo", body, headers)
    # response = cls.conn.getresponse()
    # data = response.read()
    # results = json.loads(data.decode("utf-8"))
    # print(results)
    # user_profile = Auth0.get_user_profile(id_token)
    return return_success({
        "status": True, "user_profile": user_profile})
