import re
from flask import Flask,jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

import mysql.connector
from mysql.connector.constants import ClientFlag

import random

app = Flask(__name__)
CORS(app)

INVALID_USER_ID = -1
INT_MAX_SQL = 2147483647

@app.route('/')
def index():
    return """
        Use this API to make requests for our Cards DataBase
    """

config = {
    'user': 'root',
    'password': 'cs348',
    'host': '34.70.158.171',
    'client_flags': [ClientFlag.SSL],
    'ssl_ca': 'ssl/server-ca.pem',
    'ssl_cert': 'ssl/client-cert.pem',
    'ssl_key': 'ssl/client-key.pem'
}
config['database'] = 'flashcards'  # add new database to config dict

@app.route('/user_decks/<userid>')
def get_decks(userid):
    # mysql
    cnxn = mysql.connector.connect(**config)
    cursor = cnxn.cursor()

    cursor.execute("SELECT deckid, deckname FROM decks WHERE userid=%s", (userid,))
    deck_value_arr = []
    for line in cursor:
        deck_value_arr.append(line)
    output = []
    for deck_values in deck_value_arr:
        deckid, deckname = deck_values

        # TODO: add in last_reviewed_string - how long ago this deck was last reviewed by this user as a pretty string

        # e.g. 'two days ago', 'a month ago', etc. - NOT a timestamp
        # TODO: add in num_cards
        # select count(*) from cards where deckid = %s
        cursor.execute("SELECT count(*) from cards where deckid=%s", (deckid,))
        num_cards = 0
        for line in cursor:
            num_cards = line
        deck_data = {'deckid': deckid, 'deckname': deckname, 'num_cards': num_cards[0],
                     'last_reviewed_string': 'about a week ago'}
        output.append(deck_data)

    cnxn.close()

    return jsonify({"decks": output})

@app.route('/cardhistory/<userid>')
def get_hist(userid):
    cnxn = mysql.connector.connect(**config)
    cursor = cnxn.cursor()

    cursor.execute("SELECT cardid, time FROM cardHistory WHERE userid=%s", (userid,))

    output = [{'cardid': x[0], 'userid': userid, 'time': x[1]} for x in cursor]

    cnxn.close()

    return jsonify({"cards": output})

@app.route('/bestcard/<userid>')
def get_best(userid):
    cnxn = mysql.connector.connect(**config)
    cursor = cnxn.cursor()

    cursor.execute("SELECT cardid, count(time) as a FROM cardHistory WHERE userid=%s group by cardid order by a desc limit 1", (userid,))

    output = [{'card_id': x[0], 'userid': userid, 'accesses': x[1]} for x in cursor]

    cnxn.close()

    return jsonify({"cards": output})

@app.route('/worstcard/<userid>')
def get_best(userid):
    cnxn = mysql.connector.connect(**config)
    cursor = cnxn.cursor()

    cursor.execute("SELECT cardid, count(time) as a FROM cardHistory WHERE userid=%s group by cardid order by a limit 1", (userid,))

    output = [{'card_id': x[0], 'userid': userid, 'accesses': x[1]} for x in cursor]

    cnxn.close()

    return jsonify({"cards": output})


@app.route('/deck_cards/<deckid>')
def get_deck(deckid):
    cnxn = mysql.connector.connect(**config)
    cursor = cnxn.cursor()
    
    cursor.execute("SELECT cardid, question, answer, topic FROM cards WHERE deckid=%s", (deckid, ))

    output = [{'cardid': x[0], 'deckid': deckid, 'question': x[1], 'answer': x[2], 'topic': x[3]} for x in cursor]

    cnxn.close()

    return jsonify({"cards": output})

@app.route('/createdeck', methods=['POST'])
def create_deck():
    userid = request.json['userid']
    deckname = request.json['deckname']
    cards = request.json['cards']

    cnxn = mysql.connector.connect(**config)
    cursor = cnxn.cursor(buffered=True)

    # generate deckid
    deckid = random.randint(0, INT_MAX_SQL)
    cursor.execute("SELECT * FROM decks WHERE deckid = %s", (userid, ))

    while cursor.rowcount > 0:
        deckid = random.randint(0, INT_MAX_SQL)
        cursor.execute("SELECT * FROM decks WHERE deckid = %s", (deckid, ))

    # get deckname and insert into deck
    cursor.execute("INSERT INTO decks VALUES (%s, %s, %s, %s)", (deckid, userid, deckname, userid))
    cnxn.commit()

    # insert cards
    for card in cards:
        # generate new card id
        cardid = random.randint(0, INT_MAX_SQL)
        cursor.execute("SELECT * FROM cards WHERE cardid = %s", (cardid, ))

        while cursor.rowcount > 0:
            cardid = random.randint(0, INT_MAX_SQL)
            cursor.execute("SELECT * FROM cards WHERE cardid = %s", (cardid, ))

        # insert card into deck
        data = (cardid, deckid, userid, card['question'], card['answer'], card['topic'])
        cursor.execute("INSERT INTO cards VALUES (%s, %s, %s, %s, %s, %s)", data)
    
    cnxn.commit()
    cnxn.close()

    return jsonify({"name": "success"})

@app.route('/login', methods=['POST'])
def login():
    # mysql
    username_from_user = request.json['username']
    password_from_user = request.json['password']

    cnxn = mysql.connector.connect(**config)
    cursor = cnxn.cursor()

    cursor.execute("SELECT * FROM accounts WHERE username=%s AND password=%s", (username_from_user, password_from_user))

    userid = INVALID_USER_ID
    for t in cursor:
        userid, _, _ = t

    cnxn.close()
    
    return jsonify({'status': 'OK', 'userid': userid}) if userid != INVALID_USER_ID else jsonify({'status': 'invalid'})

@app.route('/register', methods=['POST'])
def register():
    username_from_user = request.json['username']
    password_from_user = request.json['password']

    cnxn = mysql.connector.connect(**config)
    cursor = cnxn.cursor(buffered=True)

    cursor.execute("SELECT * FROM accounts WHERE username=%s", (username_from_user, ))

    userid = INVALID_USER_ID
    for t in cursor:
        userid, _, _ = t

    # username already exists
    if userid != INVALID_USER_ID:
        cnxn.close()
        return jsonify({'status': 'invalid'})

    # create new username
    else:
        # generate new userid
        userid = random.randint(0, INT_MAX_SQL)
        cursor.execute("SELECT * FROM accounts WHERE userid = %s", (userid, ))
        print(cursor.rowcount)

        while cursor.rowcount > 0:
            userid = random.randint(0, INT_MAX_SQL)
            cursor.execute("SELECT * FROM accounts WHERE userid = %s", (userid, ))

        cursor.execute("INSERT INTO accounts (userid, username, password) VALUES (%s, %s, %s)", (userid, username_from_user, password_from_user))
        cnxn.commit()
        cnxn.close()
        return jsonify({'status': 'OK', 'userid': userid})

@app.route('/cardhistory', methods=['POST'])
def cardHistory():
    cardid_from_user = request.json['cardid']
    time_from_user = request.json['time']
    userid_from_user = request.json['userid']

    cnxn = mysql.connector.connect(**config)
    cursor = cnxn.cursor(buffered=True)

    cursor.execute("INSERT INTO cardHistory (cardid, time, userid) VALUES (%s, %s, %s)", (cardid_from_user, time_from_user, userid_from_user))
    cnxn.commit()
    cnxn.close()
    return jsonify({'status': 'OK'})


