from flask import Flask, jsonify, request, render_template,Response
from pymongo import MongoClient
import pandas as pd
import json
from flask_charts import GoogleCharts
from markupsafe import Markup
from flask_charts import Chart

# from flask_rest_jsonapi import Api, ResourceDetail, ResourceList, ResourceRelationship
# from flask_rest_jsonapi.exceptions import ObjectNotFound


app = Flask(__name__)
charts = GoogleCharts(app)
df = pd.read_csv('../track_info4.csv')
df.assign(Genres=df.genres.str.split(","))
df['duration_min']= df['duration_ms'] / (1000*60)

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

@app.route('/members')
def html_members():
    return render_template('members.html')

@app.route('/duration')
def html_duration():
    return render_template('duration.html')

@app.route('/songpop')
def html_songpop():
    title = "Song Popularity"
    tracks_name_df = pd.DataFrame(df_from_mongo["track_name"].value_counts())
    tracks_name_df.rename(columns = {'track_name':'counts'},inplace=True)
    tracks_name_df['track_name'] = tracks_name_df.index

    # temps = tracks_name_df[['track_name','counts']]
    # temps['track_name'] = temps['track_name'].astype(str)

    song_pop_chart = Chart("BarChart", "songpop")
    song_pop_chart.options = {
                            "title": "Song Popularity",
                            "is3D": False,
                            "width": 500,
                            "height": 500
                        }
    song_pop_chart.data.add_column("string", "SongTitle")
    song_pop_chart.data.add_column("number", "Count")
    song_pop_chart.data.add_row([tracks_name_df['track_name'].iloc[0],200])
    song_pop_chart.data.add_row([tracks_name_df['track_name'].iloc[1],300])
    song_pop_chart.data.add_row([tracks_name_df['track_name'].iloc[2],450])
    song_pop_chart.add_event_listener("select", "my_function")
    song_pop_chart.refresh = 1000
    # d = temps.values.tolist()
    # c = temps.columns.tolist()
    # d.insert(0,c)

    # tempdata = json.dumps({'title':title,'data':d})
    
    return render_template('songpop.html',song_pop_chart = song_pop_chart)

@app.route('/topartists')
def html_topartists():
    return render_template('topartists.html')

@app.route('/topgenres')
def html_topgenres():
    return render_template('topgenres.html')

@app.route('/api/v1/songs/name',methods=['GET'])
def getsongbyname():
    args = request.args
    name = args.get('name')
    myquery = { "artists": "Taylor Swift" }
    songs_name = spotify_db.find(myquery,{'_id': 0})
    return jsonify(list(songs_name))

@app.route('/api/v1/songs/id',methods=['GET'])
def getsongbyid():
    args = request.args
    name = args.get('name')
    myquery = { "song_id": "3eX0NZfLtGzoLUxPNvRfqm" }
    songs_id = spotify_db.find(myquery,{'_id': 0})
    return jsonify(list(songs_id))

if __name__ == "__main__":
    app.run()

# class SpotifySongs:
#     __tablename__ = 


