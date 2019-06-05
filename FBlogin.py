from bottle import get, request, response, redirect
import random
import facebook

ENDPOINT_BASE_URL = 'https://www.facebook.com/v3.3/dialog/oauth'

# app info
APP_ID = '1053174974861205'
REDIRECT_URI = 'http://localhost/token'
RESPONSE_TYPE = 'token'

def build_redirect_url():
    state = str(random.randint(100_000, 1_000_000))
    return ENDPOINT_BASE_URL + '?client_id=' + APP_ID + \
            '&redirect_uri=' + REDIRECT_URI + \
            '&state=' + state + \
            '&response_type=' + RESPONSE_TYPE

@get('/login')
def login():
    print('login')
    redirect(build_redirect_url())

@get('/token')
def token():
    token = request.query['access_token']
    print('the code:', token)

def get_FBuser_id(token):
    graph = facebook.GraphAPI(access_token=token)
    profile = graph.get_object(id='me')
    id = profile['id']
    return id
