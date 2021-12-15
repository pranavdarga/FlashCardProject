from os import times
import re
from flask import Flask,jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

import mysql.connector
from mysql.connector.constants import ClientFlag

import random

import datetime
from datetime import datetime

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

    print(f'USERID = {userid}')

    cursor.execute("SELECT d1.deckid, d1.deckname FROM decks d1 JOIN DeckUsers d2 ON d1.deckid=d2.deckid WHERE d2.userid=%s;", (userid,))
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

        # get last accessed card
        cursor.execute("select ch.time from (cards c left join cardHistory ch on ch.cardid = c.cardid) where c.deckid = %s order by time desc limit 1", (deckid,))
        date = None
        for l in cursor:
            for n in l:
                date = n
        if date is None:
            #deck has never been used before
            last_used = "never"
        else:
            date_now = date.today()
            delta = date_now - date
            days_ago = delta.days
            last_used = " about " + str(days_ago) + " days ago"

        deck_data = {'deckid': deckid, 'deckname': deckname, 'num_cards': num_cards[0],
                     'last_reviewed_string': last_used}
        output.append(deck_data)

    cnxn.close()

    return jsonify({"decks": output})

# @app.route('/cardhistory/<userid>')
# def get_hist(userid):
#     cnxn = mysql.connector.connect(**config)
#     cursor = cnxn.cursor()

#     cursor.execute("SELECT cardid, time FROM cardHistory WHERE userid=%s", (userid,))

#     output = [{'cardid': x[0], 'userid': userid, 'time': x[1]} for x in cursor]

#     cnxn.close()

#     return jsonify({"cards": output})

# @app.route('/bestcard/<userid>')
# def get_best(userid):
#     cnxn = mysql.connector.connect(**config)
#     cursor = cnxn.cursor()

#     cursor.execute("SELECT cardid, count(time) as a FROM cardHistory WHERE userid=%s group by cardid order by a desc limit 1", (userid,))

#     output = [{'card_id': x[0], 'userid': userid, 'accesses': x[1]} for x in cursor]

#     cnxn.close()

#     return jsonify({"cards": output})

# @app.route('/worstcard/<userid>')
# def get_worst(userid):
#     cnxn = mysql.connector.connect(**config)
#     cursor = cnxn.cursor()

#     cursor.execute("SELECT cardid, count(time) as a FROM cardHistory WHERE userid=%s group by cardid order by a limit 1", (userid,))

#     output = [{'card_id': x[0], 'userid': userid, 'accesses': x[1]} for x in cursor]

#     cnxn.close()

#     return jsonify({"cards": output})


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
    cursor.execute("INSERT INTO decks VALUES (%s, %s, %s)", (deckid, deckname, userid))
    cnxn.commit()

    # make creator user of deck
    cursor.execute("INSERT INTO DeckUsers VALUES (%s, %s)", (userid, deckid))
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

@app.route('/user_stats/<userid>')
def user_stats(userid):
    print(f"ANALYTICS USERID = {userid}")

    cnxn = mysql.connector.connect(**config)
    cursor = cnxn.cursor(buffered=True)

    cursor.execute("select deckid, deckname from decks where userid = %s", (userid, ))
    decks = []
    for line in cursor:
        decks.append(line)

    card_table = []
    for d, deckname in decks:
        # least used card in deck
        cursor.execute("select question, answer, topic from (select c.cardid, c.deckid, c.question, c.answer, c.topic, count(time) as count from cards c left join cardHistory ch on c.cardid = ch.cardid group by c.cardid) as r join decks d on r.deckid = d.deckid where d.deckid = %s order by count limit 1;", (d, ))
        least_used_card = [t for t in cursor]
        
        # most used card in deck
        cursor.execute("select question, answer, topic from (select c.cardid, c.deckid, c.question, c.answer, c.topic, count(time) as count from cards c left join cardHistory ch on c.cardid = ch.cardid group by c.cardid) as r join decks d on r.deckid = d.deckid where d.deckid = %s order by count desc limit 1;", (d, ))
        most_used_card = [t for t in cursor]

        card_table.append([deckname, least_used_card, most_used_card])

    print("STUFF")
    print(card_table)

    #least viewed deck
    cursor.execute("select d.deckname from (select c.cardid, c.deckid, count(time) as count from cards c left join cardHistory ch on c.cardid = ch.cardid group by c.cardid) as r join decks d on r.deckid = d.deckid where userid = %s order by count limit 1", (userid, ))
    least = [{'deckname' : x[0]} for x in cursor][0]
    
    # most viewed deck
    cursor.execute("select d.deckname from (select c.cardid, c.deckid, count(time) as count from cards c left join cardHistory ch on c.cardid = ch.cardid group by c.cardid) as r join decks d on r.deckid = d.deckid where userid = %s order by count DESC limit 1", (userid, ))
    most = [{'deckname' : x[0]} for x in cursor][0]

    cnxn.close()
    return jsonify({'status': 'OK', 'least_deck': least, 'most_deck': most, 'card_table': card_table})

@app.route('/importdeck', methods=['POST'])
def importdeck():
    userid = request.json['userid']
    deckid = request.json['deckid']

    print(f'USERID = {userid} and DECKID = {deckid}')

    cnxn = mysql.connector.connect(**config)
    cursor = cnxn.cursor(buffered=True)
    
    # validate that the deckID in question exists
    cursor.execute('SELECT COUNT(*) FROM decks WHERE deckid = %s', (deckid, ))
    count = -1
    for t in cursor:
        count = t[0]

    if count < 1:
        return jsonify({'status': 'Invalid ID'})

    print(f'COUNT = {count}')

    # validate that the pairing is new
    cursor.execute('SELECT COUNT(*) FROM DeckUsers WHERE deckid = %s AND userid = %s', (deckid, userid))
    count = 0
    for t in cursor:
        count = t[0]

    if count != 0:
        return jsonify({'status': 'Entry already exists'})

    # now that those two have been established insert into table
    cursor.execute('INSERT INTO DeckUsers VALUES (%s, %s)', (userid, deckid))

    cnxn.commit()
    cnxn.close()

    return jsonify({'status': 'OK'})
