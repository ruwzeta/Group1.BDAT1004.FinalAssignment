from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient

app = Flask(__name__)

# client = MongoClient("mongodb://YCH:MON2022@ac-v9dvncc-shard-00-00.6n9k6sk.mongodb.net:27017,ac-v9dvncc-shard-00-01.6n9k6sk.mongodb.net:27017,ac-v9dvncc-shard-00-02.6n9k6sk.mongodb.net:27017/?ssl=true&replicaSet=atlas-gpgpqo-shard-0&authSource=admin&retryWrites=true&w=majority")
# db = client.FlaskApp

client = MongoClient('localhost', 27017, username='YCH', password='MON2022')

db = client.test
SpotifyData = db.Spotify2222


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run()

