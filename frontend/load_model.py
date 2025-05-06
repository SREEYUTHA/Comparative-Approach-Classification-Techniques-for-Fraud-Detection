import pickle

with open('logistic_model.sav', 'rb') as f:
    model = pickle.load(f)

