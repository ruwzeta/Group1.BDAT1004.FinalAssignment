from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient
import pandas as pd
import json

app = Flask(__name__)


df = pd.read_csv('D:/C#/FrontendFor1004/Group1.BDAT1004.FinalAssignment/track_info4.csv')
data = df.to_dict(orient = "records")

client = MongoClient("mongodb://YCH:MON2022@ac-v9dvncc-shard-00-00.6n9k6sk.mongodb.net:27017,ac-v9dvncc-shard-00-01.6n9k6sk.mongodb.net:27017,ac-v9dvncc-shard-00-02.6n9k6sk.mongodb.net:27017/?ssl=true&replicaSet=atlas-gpgpqo-shard-0&authSource=admin&retryWrites=true&w=majority")
db = client.FlaskApp

db.Spotify.insert_many(data)


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run()

