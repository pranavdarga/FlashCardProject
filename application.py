import re
from flask import Flask,jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

import mysql.connector
from mysql.connector.constants import ClientFlag

app = Flask(__name__)
CORS(app)

INVALID_USER_ID = -1

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

@app.route('/decks')
def get_decks():
    # original
    decks = Decks.query.all()
    output = []
    for deck in decks:
        deck_data = {'deckid': deck.deckid, 'deckname': deck.deckname, 'userid': deck.userid}
        output.append(deck_data)
    return {"decks": output}

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
    # get deckname and insert into deck
    
    deck = Decks(deckname=request.json['deckname'],userid=request.json['userid'])
    db.session.add(deck)
    db.session.commit()
    d = Decks.query.all()
    deckid = d[len(d)-1].deckid
    for cd in request.json['cards']:
        card = cards(cardname = cd['cardname'], deckid = deckid, question = cd['question'], answer = cd['answer'])
        db.session.add(card)
        db.session.commit()
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