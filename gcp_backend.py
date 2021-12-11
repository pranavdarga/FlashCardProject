import mysql.connector
from mysql.connector.constants import ClientFlag

config = {
    'user': 'root',
    'password': 'cs348',
    'host': '34.70.158.171',
    'client_flags': [ClientFlag.SSL],
    'ssl_ca': 'ssl/server-ca.pem',
    'ssl_cert': 'ssl/client-cert.pem',
    'ssl_key': 'ssl/client-key.pem'
}

# now we establish our connection
cnxn = mysql.connector.connect(**config)

# cursor = cnxn.cursor()  # initialize connection cursor
# cursor.execute('CREATE DATABASE flashcards')  # create a new 'testdb' database
# cnxn.close()  # close connection because we will be reconnecting to testdb

config['database'] = 'flashcards'  # add new database to config dict
cnxn = mysql.connector.connect(**config)
cursor = cnxn.cursor()

# cursor.execute('CREATE TABLE accounts (userid int, username varchar(255) NOT NULL, password varchar(255) NOT NULL, PRIMARY KEY (userid))')
cursor.execute("INSERT INTO accounts VALUES (%s, %s, %s)", (3, 'c', 'd'))
cnxn.commit()
cnxn.close()