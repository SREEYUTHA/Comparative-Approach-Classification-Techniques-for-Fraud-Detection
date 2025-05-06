import pickle

# Load the model and any additional data from the .sav file
with open('svm_model.sav', 'rb') as f:
    model_data = pickle.load(f)

# Extract the model and accuracy score
model = model_data['model']
accuracy_score = model_data['accuracy']
print(accuracy_score)