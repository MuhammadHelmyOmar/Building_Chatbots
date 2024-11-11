from schemes import load_teams_names
import textdistance
import requests
import os

api_url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
api_key = os.getenv('football_api_key', '')

headers = {
	"x-rapidapi-key": api_key,
	"x-rapidapi-host": "api-football-v1.p.rapidapi.com"
}

team_names = load_teams_names()

def get_team_id(search_name: str, threshold=0.60):
    
    found_teams = {}
    
    for team_name, team_id in team_names.items():

        sim_score = textdistance.cosine.normalized_similarity(search_name.lower(), team_name)
        
        if sim_score < threshold:
            continue

        found_teams[team_id] = sim_score
    
    if len(found_teams):
        found_teams = sorted(found_teams.items(), key=lambda item: item[1], reverse=True)
        return {
            "team_id": found_teams[0][0],
            "score": found_teams[0][1]
        }
    
    return None


def get_team_matches(team1_id: int,
                     team2_id: int = -1,
                     league_id: int = 39,
                     season: str = "2022",
                     mode: str = "last",
                     limit: int = 99):
    
    querystring = {
        "league": league_id,
        "season": season,
        "team": team1_id,
        f"{mode}": limit
    }
    
    ts = set([team1_id, team2_id])
    
    response = requests.get(api_url, headers=headers, params=querystring)
    
    if response.status_code != 200:
        return None
    
    response_data = response.json()
    
    results = []
    
    for rec in response_data["response"]:
        
        team_home = rec["teams"]["home"]
        team_away = rec["teams"]["away"]
        
        
        if team1_id > 0:
            if (int(team_home['id']) not in ts) or (int(team_away['id']) not in ts):
                continue
                 
        results.append({
            "match_date": rec["fixture"]["date"],
            "match_timezone": rec["fixture"]["timezone"],
            "team_home": team_home['name'], 
            "team_away": team_away['away'],
            "goals": rec["goals"]
        })
    
    return results