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
INT_MAXSQL = 2147483647

#set FLASK_APP=application.py
#set FLASK_ENV=development
#python
#from application import db
#db.create_all()
#from application import <tables>
#card1 = cards(cardname = "Chemistry", deckid = 2, question = "What is H2O?", answer = "Water")
#deck1 = Decks(deckname = "English", userid = 23)
#db.session.add(<row>)
#db.session.commit()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)
error_list = []

class accounts(db.Model):
    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(80), nullable=False)

class Decks(db.Model):
    deckid = db.Column(db.Integer, primary_key=True)
    deckname = db.Column(db.String(80), nullable=False)
    userid = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"{self.deckname} - {self.userid}"

class deckUsers(db.Model):
    userid = db.Column(db.Integer, primary_key=True)
    deckid = db.Column(db.Integer, primary_key=True)
    lasttime = db.Column(db.DateTime, nullable=False)

class cards(db.Model):
    cardid = db.Column(db.Integer, primary_key=True)
    cardname = db.Column(db.String(80), nullable=False)
    deckid = db.Column(db.Integer, nullable=False)
    question = db.Column(db.String(200), nullable=False)
    answer = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"{self.cardname} - {self.question} - {self.answer}"

class cardHistory(db.Model):
    cardid = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, primary_key=True)
    userid = db.Column(db.Integer, primary_key=True)

@app.route('/')
def index():
    return """
        Use this API to make requests for our Cards DataBase
    """
#
# #encrypted username/password GET
# #response: userhistory if successful else return no such user
# @app.route('/auth/<username>/<password>')
# def auth(username, password):
#     return {"userid" : username, "password" : password}
#
# #create new user POST
# #response: return success
# @app.route('/register/<username>/<password>')
# def register_user(username, password):
#     return {"errors" : error_list}
#
# #find a deck GET
# #response: deck and all the associated cards or NoSuchDeck

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

@app.route('/decks/<userid>')
def get_decks(userid):
    # mysql
    cnxn = mysql.connector.connect(**config)
    cursor = cnxn.cursor()
    
    cursor.execute("SELECT deckid, deckname FROM decks WHERE userid=%s", (userid, ))

    output = []
    for deck_values in cursor:
        deckid, deckname = deck_values
        deck_data = {'deckid': deckid, 'deckname': deckname}
        output.append(deck_data)

    cnxn.close()
    
    return jsonify({"decks": output})

@app.route('/cards')
def get_cards():
    cards1 = cards.query.all()
    output = []
    for card in cards1:
        deck_data = {'cardname': card.cardname, 'deckid': card.deckid, 'question': card.question, 'answer': card.answer}
        output.append(deck_data)
    return {"cards": output}

@app.route('/decks/<deckid>')
def get_deck(deckid):
    # original
    deck = Decks.query.get_or_404(deckid)
    # card = cards.query.all()
    # output = []
    # for c in cards:
    #     card_data = {'cardname': card.cardname, 'question': card.question, 'answer': card.answer}
    #     output.append(card_data)

    cards1 = cards.query.all()
    output = []
    for card in cards1:
        if int(card.deckid) == int(deckid):
            deck_data = {'cardname': card.cardname, 'deckid': card.deckid, 'question': card.question, 'answer': card.answer}
            output.append(deck_data)
    #return {"cards": output}
    return {"deckname": deck.deckname, "userid": deck.userid, "cards": output}

    # return {"deckname": deck.deckname, "userid": deck.userid}
#create a deck POST
#response: success or unsuccessful
#from application import <tables>
#card1 = cards(cardname = "Chemistry", deckid = 2, question = "What is H2O?", answer = "Water")
#deck1 = Decks(deckname = "English", userid = 23)
#db.session.add(<row>)
#db.session.commit()
@app.route('/createdeck', methods=['POST'])
def create_deck():
    userid = request.json['userid']
    deckname = request.json['deckname']
    cards = request.json['cards']

    cnxn = mysql.connector.connect(**config)
    cursor = cnxn.cursor(buffered=True)

    # generate deckid
    deckid = random.randint(0, INT_MAXSQL)
    cursor.execute("SELECT * FROM decks WHERE deckid = %s", (userid, ))

    while cursor.rowcount > 0:
        deckid = random.randint(0, INT_MAXSQL)
        cursor.execute("SELECT * FROM decks WHERE deckid = %s", (deckid, ))

    # get deckname and insert into deck
    cursor.execute("INSERT INTO decks VALUES (%s, %s, %s, %s)", (deckid, userid, deckname, userid))
    cnxn.commit()

    # insert cards
    for card in cards:
        # generate new card id
        cardid = random.randint(0, INT_MAXSQL)
        cursor.execute("SELECT * FROM cards WHERE cardid = %s", (cardid, ))

        while cursor.rowcount > 0:
            cardid = random.randint(0, INT_MAXSQL)
            cursor.execute("SELECT * FROM cards WHERE cardid = %s", (cardid, ))

        # insert card into deck
        data = (cardid, deckid, userid, card['question'], card['answer'], card['topic'])
        cursor.execute("INSERT INTO cards VALUES (%s, %s, %s, %s, %s, %s)", data)
    
    cnxn.commit()
    cnxn.close()
    # deck = Decks(deckname=request.json['deckname'],userid=request.json['userid'])
    # db.session.add(deck)
    # db.session.commit()
    # d = Decks.query.all()
    # deckid = d[len(d)-1].deckid
    # for cd in request.json['cards']:
    #     card = cards(cardname = cd['cardname'], deckid = deckid, question = cd['question'], answer = cd['answer'])
    #     db.session.add(card)
    #     db.session.commit()
    #db.session.commit()

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