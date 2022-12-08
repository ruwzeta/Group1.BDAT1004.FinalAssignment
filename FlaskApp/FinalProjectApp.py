from flask import Flask, jsonify, request, render_template,Response
from pymongo import MongoClient
import pandas as pd
import json

app = Flask(__name__)

# Inserting Data into MongoDB using Collected Data from Spotify API 
# df = pd.read_csv('../track_info4.csv')
# df.assign(Genres=df.genres.str.split(","))
# df['duration_min']= df['duration_ms'] / (1000*60)
# df2 = df.assign(Genres=df.genres.str.split(",")).explode('Genres')
# data = df.to_dict(orient = "records")

# MongDB Connection
client = MongoClient("mongodb://YCH:MON2022@ac-v9dvncc-shard-00-00.6n9k6sk.mongodb.net:27017,ac-v9dvncc-shard-00-01.6n9k6sk.mongodb.net:27017,ac-v9dvncc-shard-00-02.6n9k6sk.mongodb.net:27017/?ssl=true&replicaSet=atlas-gpgpqo-shard-0&authSource=admin&retryWrites=true&w=majority")
db = client.BDAT1004_Final2

spotify_db = db.SongData
#spotify_db.insert_many(data)

# Retrieve Data from MongoDB (All data)
cursor=spotify_db.find()
list_cur = list(cursor)
df_from_mongo = pd.DataFrame(list_cur)

## Web Page Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/datatable', methods=("POST", "GET"))
def html_table():
    return render_template('data.html',  tables=[df_from_mongo.to_html(classes='data')], titles=df_from_mongo.columns.values)

@app.route('/members')
def html_members():
    return render_template('members.html')

@app.route('/duration')
def html_duration():

    temps = df_from_mongo[['duration_min','popularity']]
    d = temps.values.tolist()
    c = temps.columns.tolist()
    d.insert(0,c)

    tempdata = json.dumps({'data':d})

    return render_template('duration.html',tempdata = tempdata)

@app.route('/songpop')
def html_songpop():
    tracks_name_df = pd.DataFrame(df_from_mongo["track_name"].value_counts())
    tracks_name_df.rename(columns = {'track_name':'counts'},inplace=True)
    tracks_name_df['track_name'] = tracks_name_df.index
    temps = tracks_name_df[['track_name','counts']]
    temps['track_name'] = temps['track_name'].astype(str)
    d = temps.values.tolist()
    c = temps.columns.tolist()
    d.insert(0,c)

    tempdata = json.dumps({'data':d})
    
    return render_template('songpop.html',tempdata = tempdata)

@app.route('/topartists')
def html_topartists():
    
    df2 = df_from_mongo.assign(Artists=df_from_mongo['artists'].str.split(",")).explode('artists')
    df2["id"] = df2.index + 1
    artists_count = df2.groupby(["artists"]).count()
    artists_count['count'] = artists_count.id
    artists_count['Artists'] = artists_count.index
    artists_count['Artists'] = artists_count['Artists'].str.replace(" ", "")

    temps = artists_count[['Artists','count']].sort_values(['count'],ascending=False).head(10)
    temps['Artists'] = temps['Artists'].astype(str)
    d = temps.values.tolist()
    c = temps.columns.tolist()
    d.insert(0,c)

    tempdata = json.dumps({'data':d})
    return render_template('topartists.html',tempdata = tempdata)

@app.route('/topgenres')
def html_topgenres():

    df2 = df_from_mongo.assign(Genres=df_from_mongo['genres'].str.split(",")).explode('Genres')
    df2["id"] = df2.index + 1
    genres_count = df2.groupby(["Genres"]).count()
    genres_count['count'] = genres_count.id
    genres_count['Genres'] = genres_count.index
    genres_count['Genres'] = genres_count['Genres'].str.replace(" ", "")

    temps = genres_count[['Genres','count']].sort_values(['count'],ascending=False).head(10)
    temps['Genres'] = temps['Genres'].astype(str)
    d = temps.values.tolist()
    c = temps.columns.tolist()
    d.insert(0,c)

    tempdata = json.dumps({'data':d})
    return render_template('topgenres.html',tempdata = tempdata)

## API routes
@app.route('/api/v1/songs/all',methods=['GET'])
def allsongs():
    songs = spotify_db.find([], {'_id': 0})
    return jsonify(list(songs))

@app.route('/api/v1/songs/name',methods=['GET'])
def getsongbyname():
    args = request.args
    name = args.get('name')
    myquery = { "artists": name }
    songs_name = spotify_db.find(myquery,{'_id': 0})
    return jsonify(list(songs_name))

@app.route('/api/v1/songs/id',methods=['GET'])
def getsongbyid():
    args = request.args
    id = args.get('id')
    myquery = { "song_id": id }
    songs_id = spotify_db.find(myquery,{'_id': 0})
    return jsonify(list(songs_id))

if __name__ == "__main__":
    app.run()



