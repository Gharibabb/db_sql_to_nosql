from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from db_connection import db, match_information, match_events, match_line_ups, match_player_statistics, match_team_statistics
from bson.objectid import ObjectId
import pandas as pd

app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route('/players', methods=['GET'])
def get_players():

    players = list(match_information.find({},{"HomeTeamName":1, "_id":0}))
    return render_template('players.html', players=players)

#Selectionner le nombre de bléssures qu'il y'a eu pendant toute la compétion en les regroupants par étape
@app.route('/blessures', methods=['GET'])
def get_nb_blessures():
    nb_blessures = { "$group" : {"_id" : "$RoundName", "totalBlessures" : { "$sum" : "$InjuryTime" }} }
    aggregate = list(match_information.aggregate([nb_blessures]))
    print(a[0])
    return render_template("player.html",player=aggregate)


@app.route('/win', methods=['GET'])
def get_match_won():
    aggregate = list(match_information.find({
    "RoundName": {
    "$in": ["quarter finals", "semi finals", "final"]},
    "$or": [
        { "$expr": { "$gte": [ { "$subtract": ["$ScoreHome", "$ScoreAway"] }, 1 ] } },
        { "$expr": { "$gte": [ { "$subtract": ["$ScoreAway", "$ScoreHome"] }, 1 ] } }
    ]},
    {
        "HomeTeamName": 1,
        "awayteamname": 1,
        "RoundName": 1,
        "ScoreHome": 1,
        "ScoreAway": 1,
        "_id": 0
    }
    ))
    print(aggregate)
    return render_template("won.html", won=aggregate)

@app.route('/quarterfinales', methods=['GET'])
def get_quarter_finales():
    query = {"RoundName": "final tournament", 
         "$or": [{"ScoreHome": {"$gt": 0}}, {"ScoreAway": {"$gt": 0}}], 
         "$or": [{"HomeTeamName": {"$in": match_information.distinct("HomeTeamName", {"RoundName": "quarter finals"})}}, 
                 {"AwayTeamName": {"$in": match_information.distinct("AwayTeamName", {"RoundName": "quarter finals"})}}]}

    # exécuter la requête et stocker les résultats dans un DataFrame pandas
    aggregate = list(match_information.find(query, {"_id":0,"HomeTeamName": 1, "AwayTeamName": 1, "RoundName": 1, "ScoreHome": 1, "ScoreAway": 1}))

    return render_template("quarterfinales.html", quarter=aggregate)


@app.route('/scored', methods=['GET'])
def get_goal():
    #Trouvez les joueurs qui ont marqué un but contre l'équipe tenante du titre (Portugal) 
    #pendant la phase de groupes.  

    aggregate = list(match_information.aggregate([
            {"$match":{"$or": [{"HomeTeamName": 'Portugal', "IsAwayTeam": True },
                        { "AwayTeamName": 'Portugal', "IsHomeTeam": True}
                        ],
                "GoalScored": {"$gte":1}
                }
            },
            {"$project": {"_id": 0,"HomeTeamName": 1,"AwayTeamName": 1,"IsHomeTeam": 1,"ShortName": 1,"GoalScored": 1}}
        ])
    )

    return render_template("goal.html", scored=aggregate)

@app.route('/redcards', methods=['GET'])
def get_red_cards():
        # specify the collection 
    collection = db.match_player_statistics
    # build the query 
    query = { "StatsName": "Red cards" }
    # use the distinct method to get the count of unique playerids 
    count = len(collection.distinct("PlayerID", query))
    # print the result
    return render_template("redcards.html", redcards=count)
