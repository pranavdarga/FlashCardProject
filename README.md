# FlashCardProject Python

1.
```
pip install -r requirements.txt
```
This installs dependancies

2. 
```
export FLASK_APP=main.py
export FLASK_ENV=development
flask run
```

# React

```
cd flashcards-frontend
yarn install
npm start

```

# For Google Cloud
Connect via terminal: Make sure you're in the root directory. Then,

```
mysql -uroot -p -h 34.70.158.171 --ssl-ca=ssl/server-ca.pem --ssl-cert=ssl/client-cert.pem --ssl-key=ssl/client-key.pem
```

Password is `cs348`.

Then, type `use flashcards`.

https://console.cloud.google.com/sql/instances/cs-348-flashcards/databases?project=shatayu-348