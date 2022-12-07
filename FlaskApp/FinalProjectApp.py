from flask import Flask, jsonify, request, render_template,Response
from pymongo import MongoClient
import pandas as pd
import json

# from flask_rest_jsonapi import Api, ResourceDetail, ResourceList, ResourceRelationship
# from flask_rest_jsonapi.exceptions import ObjectNotFound


app = Flask(__name__)
df = pd.read_csv('../track_info4.csv')
df.assign(Genres=df.genres.str.split(","))
df['duration_min']= df['duration_ms'] / (1000*60)

df2 = df.assign(Genres=df.genres.str.split(",")).explode('Genres')

data = df.to_dict(orient = "records")

client = MongoClient("mongodb://YCH:MON2022@ac-v9dvncc-shard-00-00.6n9k6sk.mongodb.net:27017,ac-v9dvncc-shard-00-01.6n9k6sk.mongodb.net:27017,ac-v9dvncc-shard-00-02.6n9k6sk.mongodb.net:27017/?ssl=true&replicaSet=atlas-gpgpqo-shard-0&authSource=admin&retryWrites=true&w=majority")
db = client.FlaskApp1004


spotify_db = db.Spotify
spotify_db.insert_many(data)

# cursor=spotify_db.find()
# docs=list(cursor)



@app.route('/')
def index():
    return render_template('index.html')


# @app.route('/allsongs',methods=['GET'])
# def allsongs():
#     return jsonify(docs)


if __name__ == "__main__":
    app.run()

# class SpotifySongs:
#     __tablename__ = 


