from bson import ObjectId
from pymongo import MongoClient

client = MongoClient('mongodb+srv://Sham:LwNIklUIvNYefZO5@cluster0.kxvrnx9.mongodb.net/test', 27017) # connect to MongoDB server
db = client['Euro2020'] # select the database
#Collections
match_information = db['match_information'] 
match_events = db['match_events'] 
match_line_ups = db['match_line_ups'] 
match_player_statistics = db['match_player_statistics'] 
match_team_statistics = db['match_team_statistics'] 
pre_match_information = db['pre_match_information']
