from flask import Flask, render_template, redirect
import urllib.request, json 
from datetime import datetime
from pytz import timezone
import pytz

app = Flask(__name__)

def refresh_data(link):
    with urllib.request.urlopen(link) as url:
        return json.loads(url.read().decode())

@app.route('/<string:datestring>/<string:gamestring>') 
def game(datestring, gamestring): 
    
    pbp = "https://data.nba.net/data/10s/json/cms/noseason/game/{}/{}/pbp_all.json".format(datestring, gamestring)
    with urllib.request.urlopen(pbp) as url:
        plays = json.loads(url.read().decode())
    if "play" in plays["sports_content"]["game"]:
        return render_template('game.html', plays = plays["sports_content"]["game"]["play"], datestring = datestring, gamestring = gamestring,
        visitor = plays["sports_content"]["game"]["game_url"][-6:-3], home = plays["sports_content"]["game"]["game_url"][-3:])
    else:
        return render_template('game.html', plays = {}, datestring = datestring, gamestring = gamestring,
        visitor = plays["sports_content"]["game"]["game_url"][-6:-3], home = plays["sports_content"]["game"]["game_url"][-3:])


@app.route('/<string:datestring>') 
def scoreboard(datestring): 
    scoreboard = "https://data.nba.net/prod/v1/{}/scoreboard.json".format(datestring)
    with urllib.request.urlopen(scoreboard) as url:
        scores = json.loads(url.read().decode())
    
    return render_template('get_json.html', scores = scores["games"], datestring = datestring)

@app.route('/')
def index():
    date = datetime.now(tz=pytz.utc)
    dt = date.astimezone(timezone('US/Pacific'))
    datestring = "{}{}{}".format(f"{dt.year:02}", f"{dt.month:02}", f"{dt.day:02}")
    return scoreboard(datestring)
    #return redirect("/"+datestring, code=302)

@app.route('/test') 
def test(): 
    return render_template('get_json.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000)