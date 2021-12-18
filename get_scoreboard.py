# -*- coding: utf-8 -*-
"""
Created on Sun Dec 12 13:03:15 2021

@author: arvin
"""

import urllib.request, json 

scoreboard = "https://data.nba.net/prod/v1/20211212/scoreboard.json"
pbp = "https://data.nba.net/data/10s/json/cms/noseason/game/20211212/0022100403/pbp_all.json"

with urllib.request.urlopen(scoreboard) as url:
    scores = json.loads(url.read().decode())

with urllib.request.urlopen(pbp) as url:
    plays = json.loads(url.read().decode())

import json
import time
from datetime import datetime

    
def refresh_data(link):
    with urllib.request.urlopen(link) as url:
        return json.loads(url.read().decode())

def get_scores(data):
    scoreline = ""
    for item in data["games"]:
        scoreline += item["vTeam"]["triCode"] + " " + item["vTeam"]["score"] + " " + item["hTeam"]["triCode"] + " " + item["hTeam"]["score"] + "\n"
    return scoreline

def get_last_play(data):
    return data["sports_content"]["game"]["play"][-1]["description"]
    

while True:
    print(datetime.now())
    last_play = get_last_play(plays)
    print(get_last_play(plays))
    #print(get_scores(scores))
    plays = refresh_data(pbp)
    time.sleep(0.5)
    