import requests
import json


# MAKE API CALLS

def makeAPICalls(url, endpointParams, debug = 'no'):
    data = requests.get(url, endpointParams)
    #print(json.loads(data.content))
    return json.loads(data.content)


# CREDENTIALS

def getCreds():
    params = dict()
    params['client_id'] = '1111111111'                  # client id
    params['client_secret'] = 'abcdef123456'     # client secret
    params['graph_domain'] = 'https://graph.facebook.com'
    params['graph_version'] = 'v13.0'
    params['endpoint_base'] = params['graph_domain'] + '/' + params['graph_version'] + '/'
    params['debug'] = 'no'
    params['redirect_uri'] = ''
    params['code'] = ''
    params['access_token'] = ''        # access token
    params['user_id'] = '11111111'      # app user id
    return params


# EXCHANGE CODE FOR ACCESS TOKEN

def getAccessToken(params, code):
    endpointParams = dict()
    url = params['endpoint_base'] + 'oauth/access_token'
    endpointParams['redirect_uri'] = '' # redirect uri
    endpointParams['client_id'] = params['client_id']
    endpointParams['client_secret'] = params['client_secret']
    endpointParams['code'] = code
    return makeAPICalls(url, endpointParams)    


# GET DEBUG TOKENS AND USER ID

def getDebugToken(params, access_token):
    # Define Endpoint Parameters
    endpointParams = dict()
    endpointParams['input_token'] = params['access_token']
    endpointParams['access_token'] = access_token
    url = params['graph_domain'] + '/debug_token'
    return makeAPICalls(url, endpointParams)


# GET INSTAGRAM USER ID AND NAME

def getInstagramCreds(params):
    #url = 'https://graph.instagram.com/' + params['graph_version'] + '/' + params['user_id']
    url = params['graph_domain'] + '/' + params['graph_version'] + '/' + params['user_id']
    endpointParams = dict() 
    endpointParams['fields'] = 'id,username'
    endpointParams['access_token'] = params['access_token']
    return makeAPICalls(url, endpointParams)        


# EXCHANGE ACCESS TOKENS TO LIFETIME

def getLifetimeToken(params, access_token):
    endpointParams = dict() 
    endpointParams['grant_type'] = 'fb_exchange_token'
    endpointParams['client_id'] = params['client_id']
    endpointParams['client_secret'] = params['client_secret']
    endpointParams['fb_exchange_token'] = access_token
    url = params['endpoint_base'] + 'oauth/access_token'
    return makeAPICalls(url, endpointParams)


# GET INSIGHTS ON IG USER

def getInsights(params, instagram_account_id):
    url = params['endpoint_base'] + str(instagram_account_id) + '/insights'
    endpointParams = dict()
    endpointParams['metric'] = 'impressions,reach,profile_views,website_clicks'
    endpointParams['period'] = 'lifetime' 
    endpointParams['access_token'] = params['access_token'] 
    return makeAPICalls(url, endpointParams)
