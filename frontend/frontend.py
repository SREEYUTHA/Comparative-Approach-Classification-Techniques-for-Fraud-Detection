from flask import Flask, render_template, request
import pickle
from sklearn.metrics import accuracy_score

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    type = request.form['type']
    amount = float(request.form['amount'])
    oldBalanceOrig = float(request.form['oldBalanceOrig'])
    newBalanceOrig = float(request.form['newBalanceOrig'])
    isFlaggedFraud = float(request.form['isFlaggedFraud'])

    if type == "CASH IN":
        lis = [1, 0, 0, 0, 0]
    elif type == "CASH OUT":
        lis = [0, 1, 0, 0, 0]
    elif type == "DEBIT":
        lis = [0, 0, 1, 0, 0]
    elif type == "PAYMENT":
        lis = [0, 0, 0, 1, 0]
    elif type == "TRANSFER":
        lis = [0, 0, 0, 0, 1]
    else:
        lis = [0, 0, 0, 0, 0]

    lis.extend([amount, oldBalanceOrig, newBalanceOrig, isFlaggedFraud])

    # Load selected model
    choice = request.form['model']
    if choice == "LOGISTIC":
        loaded_model = pickle.load(open('logistic_model.sav', 'rb'))
    elif choice == "Decision Trees":
        loaded_model = pickle.load(open('decision_model.sav', 'rb'))
        #accuracy = loaded_model.accuracy
    elif choice == "SVM":
        loaded_model = pickle.load(open('svm_model.sav', 'rb'))
        #accuracy = loaded_modelmodel['accuracy']
    else:
        return "Invalid Model Selection"


    # Predict
    pred = loaded_model.predict([lis])


    result = "Fraud Transaction" if pred[0] == 1 else "Not a Fraud Transaction"

    accuracy = ''
    if 'accuracy' in globals():
        accuracy = f"Model Accuracy: {accuracy:.2f}"

    return render_template('index.html', result=result, accuracy=accuracy)

    '''
    if pred[0] == 1:
        return "Fraud Transaction"
    else:
        return "Not a Fraud Transaction"

    if accuracy:
        return f"{result}, Model Accuracy: {accuracy:.2f}"
    else:
        return result
    #accuracy = accuracy_score(y_test, y_pred)

    #return f"Accuracy: {accuracy}"
    '''



if __name__ == '__main__':
    app.run(debug=True)