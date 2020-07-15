import requests as request
import webbrowser
import json
import os.path
from termcolor import colored

import utils

client_id='3583'
secret='HRoz3Ci7b1omjqUFZDtZjmjZnTfXz7dEUFAMLGiD'
redirect_uri='https://anilist.co/api/v2/oauth/pin'

def getAuth():
    print(colored('[Info]', 'blue'), 'Getting Authorization')
    url = f'https://anilist.co/api/v2/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code'
    webbrowser.open(url)
    print(colored('[Info]', 'blue'),'Paste the code provided')
    code = input(colored('>', 'yellow'))
    getAccessToken(code)

def getAccessToken(code):
    print(colored('[Info]', 'blue'), 'Getting Access Token')
    url='https://anilist.co/api/v2/oauth/token'
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    params = {
        'grant_type': 'authorization_code',
        'client_id': client_id,
        'client_secret': secret,
        'redirect_uri': redirect_uri,
        'code': code,
    }
    response = request.post(url, headers=headers, json=params)
    response = json.loads(response.text)
    utils.writetoken(response["access_token"])

def AccessToken():
    if os.path.exists('AccessToken.dat'):
        token = utils.readtoken()
    else:
        getAuth()
        token = utils.readtoken()
    return token