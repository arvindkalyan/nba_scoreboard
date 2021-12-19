from flask import Flask, render_template
import urllib.request, json 

app = Flask(__name__)

def get_scores(data):
    scoreline = ""
    for item in data["games"]:
        scoreline += item["vTeam"]["triCode"] + " " + item["vTeam"]["score"] + " " + item["hTeam"]["triCode"] + " " + item["hTeam"]["score"] + "\n"
    return scoreline



@app.route('/')
def index():
    scoreboard = "https://data.nba.net/prod/v1/20211212/scoreboard.json"
    with urllib.request.urlopen(scoreboard) as url:
        scores = json.loads(url.read().decode())
    return render_template('index.html', scores = scores["games"])