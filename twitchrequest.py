#getting requests from twitch api

import requests
import json
import tokens

BASE_URL = 'https://api.twitch.tv/helix/'

HEADERS = {
    'Client-ID': tokens.client_id,
    'Authorization': 'Bearer ' + tokens.access_token
}
INDENT = 2

def get_response(query):
    url = BASE_URL + query
    response = requests.get(url, headers=HEADERS)
    return response

def print_response(response):
    response_json = response.json()
    print_response = json.dumps(response_json,indent=INDENT)
    print(print_response)

def get_user_query(user_login):
    return f'users?login={user_login}'

def when_created(user_login):
    query = get_user_query(user_login)
    try:
        response = get_response(query)
        response_json = response.json()
        return response_json['data'][0]['created_at'][:10]
    except:
        return 'Użytkownik nie istnieje'

def get_user_id(user_login):
    query = get_user_query(user_login)
    try:
        response = get_response(query)
        response_json = response.json()
        return response_json['data'][0]['id']
    except:
        return 'Użytkownik nie istnieje'

def since_when_follow(from_user_id,to_user_id):
    if from_user_id == to_user_id:
            return 'Nie mozna followowac samego siebie'
    query = get_user_follows(from_user_id,to_user_id)
    try:
        response = get_response(query)
        response_json = response.json()
        
        return response_json['data'][0]['followed_at'][:10]
    except:
        return 'Nie followuje'
   
def get_user_follows(from_user_id,to_user_id):
    return f'users/follows?from_id={from_user_id}&to_id={to_user_id}'