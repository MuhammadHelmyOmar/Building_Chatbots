# Entry gate for the web component

from fastapi import FastAPI, Response
from schemes import Message, Team
from resources import load_models
from league import get_team_id, get_team_matches


models = load_models()
app = FastAPI()

# entry endpoint
@app.get('/')
async def root():
    return {"message": "Welcome World!"}

@app.post("/nlu/parse")
async def chatbot_parse(message: Message, response: Response):
    
    if message.text.strip() == "" or message.text is None:
        response.status_code = 400
        return {"error": "You must provide a text"}
    
    intent_probs = models["intent_detection"].predict_proba(message.text).tolist()
    max_prob_value = max(intent_probs)
    max_prob_idx = intent_probs.index(max_prob_value)
    intent_name = message.intent_labels[max_prob_idx]
    
    entities = models["entity_recognition"].predict_entities(message.text, message.entity_labels)
    entities_values = []
    
    for ent in entities:
        
        value_id = None
        
        if ent["label"] == "team_name":
            value_id = get_team_id(search_name=ent["text"])
        
        entities_values.append({
            "entity": ent["label"],
            "start": ent["start"],
            "end": ent["end"],
            "confidence_entity": ent["score"],
            "value": ent["text"],
            "extractor": "_",
            "value_id": value_id
        })
    
    return {
        "results": {
            
            "text": message.text,
            
            "intent": {
                "name": intent_name,
                "confidence": max_prob_value
            },
            
            "entities": entities_values
        }
    }
 
    
@app.post("/league/team_next_match")
async def team_next_match(team: Team, response: Response):
    matches = get_team_matches(team1_id=team.team1_id, team2_id=team.team2_id, mode="next")
    
    return {"results": matches}

@app.post("/league/team_last_match")
async def team_last_match(team: Team, response: Response):
    matches = get_team_matches(team1_id=team.team1_id, team2_id=team.team2_id, mode="last")
    
    return {"results": matches}
    