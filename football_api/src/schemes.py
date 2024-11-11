from pydantic import BaseModel
from typing import Optional

class Message(BaseModel):
    text: str
    intent_labels = [
        "greet-hi",
        "greet-who_are_you",
        "greet-good_bye",
        "matches-team_next_match",
        "matches-match_time", 
        "matches-match_result"
    ]
    entity_labels = ["team_name"]
    
class Team(BaseModel):
    team1_id: int
    team2_id: Optional[int] = -1
    
def load_teams_names():
#     # Map between team names and codes
    premier_league_clubs = {
        'manchester united': 33, 'mun': 33, 
        'newcastle': 34, 'new': 34, 
        'bournemouth': 35, 'bou': 35, 
        'fulham': 36, 'ful': 36, 
        'wolves': 39, 'wol': 39, 
        'liverpool': 40, 'liv': 40, 
        'southampton': 41, 'sou': 41, 
        'arsenal': 42, 'ars': 42, 
        'everton': 45, 'eve': 45, 
        'leicester': 46, 'lei': 46, 
        'tottenham': 47, 'tot': 47, 
        'west ham': 48, 'wes': 48, 
        'chelsea': 49, 'che': 49, 
        'manchester city': 50, 'mac': 50, 
        'brighton': 51, 'bri': 51, 
        'crystal palace': 52, 'cry': 52, 
        'brentford': 55, 'bre': 55, 
        'leeds': 63, 'lee': 63, 
        'nottingham forest': 65, 'not': 65, 
        'aston villa': 66, 'ast': 66
    }
    
    return premier_league_clubs