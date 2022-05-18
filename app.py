from flask import Flask, request, jsonify
import json
import sqlite3
from instagram_analytics import *

app = Flask(__name__)

def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("ig_data.sqlite")
    except sqlite3.error as e:
        print(e)
    return conn

@app.route("/", methods = ["GET"])
def getURI():
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == "GET":
        cursor = conn.execute("SELECT * FROM app_user")
        data = [
            dict(id=row[0], user_id = row[3])
            for row in cursor.fetchall()
        ]

        if data is not None:
            return jsonify(data)

        return {"status": "ok"}


@app.route("/access_token")
def access_token():
    try:
        print('access_token running...')
        print("request.args : ", request.args)
        print("request.args['access_token']", request.args['access_token'])
        access_token = request.args['access_token']
        return {"access_token": access_token}
    except:
        return {"access_token": None}        


@app.route("/callback_token")
def callback_token():
    print('callback_token running...')
    print("request.args : ", request.args)
    if request.args['code'] is not None:
        print("request.args['code'] :", request.args['code'])
        code = request.args['code']
        print('code : ', code)
        params = getCreds()
        token_json = getAccessToken(params, code)
        print(token_json)
        access_token = token_json['access_token']
        print('access_token : ', access_token)
        life_access_token_json = getLifetimeToken(params, access_token)
        print('life_access_token_json : ', life_access_token_json)
        access_token = life_access_token_json['access_token']
        print('life_access_token : ', access_token)
        debug_json = getDebugToken(params, access_token)
        #user_id = debug_json['data']['user_id']
        #print('user_id : ', user_id)

        ## UPDATE DB
        '''
        conn = db_connection()
        cursor = conn.cursor()
        sql = """INSERT INTO app_user(code, access_token, user_id, instagram_account_id)
        """
        cursor = cursor.execute(sql, (code, access_token, user_id, ''))
        conn.commit()
        '''

    return {"status": "success"}         


if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8080, debug=True) 