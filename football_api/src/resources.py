from setfit import SetFitModel
from gliner import GLiNER
import os
from functools import lru_cache

@lru_cache(maxsize=None)
def load_models():
    
    hf_token = os.getenv("hf_token", None) # None is the default value
    setfit_model_id = os.getenv("setfit_model_id", "MuhammadHelmy/botpress_football_sft_model")
    gliner_model_id = os.getenv("gliner_model_id", "urchade/gliner_multi-v2.1")
    
    models = {
        "intent_detection": SetFitModel.from_pretrained(setfit_model_id, token = "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"),
        "entity_recognition": GLiNER.from_pretrained(gliner_model_id)
    }
    
    return models