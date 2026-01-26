# sample_pickle_load.py
import pickle

def load_data(path: str):
    with open(path, "rb") as f:
        obj = pickle.load(f)  
    return obj

def harmless():
    return {"ok": True}
