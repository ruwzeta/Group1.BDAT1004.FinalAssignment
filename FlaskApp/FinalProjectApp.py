from flask import Flask, jsonify, request, render_template,Response
from pymongo import MongoClient
import pandas as pd
import json

# from flask_rest_jsonapi import Api, ResourceDetail, ResourceList, ResourceRelationship
# from flask_rest_jsonapi.exceptions import ObjectNotFound


app = Flask(__name__)
#df = pd.read_csv('../track_info4.csv')
# df.assign(Genres=df.genres.str.split(","))
# df['duration_min']= df['duration_ms'] / (1000*60)

# df2 = df.assign(Genres=df.genres.str.split(",")).explode('Genres')

# data = df.to_dict(orient = "records")

client = MongoClient("mongodb://YCH:MON2022@ac-v9dvncc-shard-00-00.6n9k6sk.mongodb.net:27017,ac-v9dvncc-shard-00-01.6n9k6sk.mongodb.net:27017,ac-v9dvncc-shard-00-02.6n9k6sk.mongodb.net:27017/?ssl=true&replicaSet=atlas-gpgpqo-shard-0&authSource=admin&retryWrites=true&w=majority")
db = client.FlaskApp1004


spotify_db = db.Spotify
#spotify_db.insert_many(data)

cursor=spotify_db.find()
list_cur = list(cursor)
df_from_mongo = pd.DataFrame(list_cur)



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/v1/songs/all',methods=['GET'])
def allsongs():
    songs = spotify_db.find({}, {'_id': 0})
    return jsonify(list(songs))

@app.route('/datatable', methods=("POST", "GET"))
def html_table():
    return render_template('data.html',  tables=[df_from_mongo.to_html(classes='data')], titles=df_from_mongo.columns.values)

@app.route('/api/v1/songs/name',methods=['GET'])
def getsongbyname():
    myquery = { "artists": "Taylor Swift" }
    songs_name = spotify_db.find(myquery,{'_id': 0})
    return jsonify(list(songs_name))

@app.route('/api/v1/songs/id',methods=['GET'])
def getsongbyid():
    myquery = { "song_id": "3eX0NZfLtGzoLUxPNvRfqm" }
    songs_id = spotify_db.find(myquery,{'_id': 0})
    return jsonify(list(songs_id))

if __name__ == "__main__":
    app.run()

# class SpotifySongs:
#     __tablename__ = 


