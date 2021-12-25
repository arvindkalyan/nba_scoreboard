from flask import Flask, render_template, redirect
import urllib.request, json 
from datetime import datetime, timedelta
from pytz import timezone
import pytz

app = Flask(__name__)

def refresh_data(link):
    with urllib.request.urlopen(link) as url:
        return json.loads(url.read().decode())

@app.route('/<string:datestring>/<string:gamestring>/box') 
def box(datestring, gamestring): 
    
    boxscore = "https://data.nba.net/prod/v1/{}/{}_boxscore.json".format(datestring, gamestring)
    with urllib.request.urlopen(boxscore) as url:
        box = json.loads(url.read().decode())
    if "stats" in box:
        return render_template('box.html', activePlayers=box["stats"]["activePlayers"], datestring = datestring, gamestring = gamestring, 
            visitor=box["basicGameData"]["vTeam"]["triCode"], home=box["basicGameData"]["hTeam"]["triCode"],
            vID=box["basicGameData"]["vTeam"]["teamId"], hID=box["basicGameData"]["hTeam"]["teamId"])
    else:
        return render_template('box.html', activePlayers={}, datestring = datestring, gamestring = gamestring, 
            visitor=box["basicGameData"]["vTeam"]["triCode"], home=box["basicGameData"]["hTeam"]["triCode"],
            vID=box["basicGameData"]["vTeam"]["teamId"], hID=box["basicGameData"]["hTeam"]["teamId"])


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
    da = datetime.strptime(datestring, "%Y%m%d")+timedelta(1)
    db = datetime.strptime(datestring, "%Y%m%d")-timedelta(1)

    before = "{}{}{}".format(f"{db.year:02}", f"{db.month:02}", f"{db.day:02}")
    after = "{}{}{}".format(f"{da.year:02}", f"{da.month:02}", f"{da.day:02}")
    return render_template('scoreboard.html', scores = scores["games"], datestring = datestring, before=before, after=after)

@app.route('/')
def index():
    date = datetime.now(tz=pytz.utc)
    dt = date.astimezone(timezone('US/Pacific'))
    datestring = "{}{}{}".format(f"{dt.year:02}", f"{dt.month:02}", f"{dt.day:02}")
    return scoreboard(datestring)
    #return redirect("/"+datestring, code=302)

@app.route('/test') 
def test(): 
    return render_template('scoreboard.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000)