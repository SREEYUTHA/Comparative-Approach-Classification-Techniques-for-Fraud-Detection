import imp
from numpy import size
import streamlit as st 
import requests
from streamlit_lottie import st_lottie
import pickle
import pandas as pd

st.set_page_config(page_title = "Fraud transaction Detection",layout = "wide")
st.title("Fraud Transaction Detection")

def load_lottie(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

topProduct = load_lottie("https://assets9.lottiefiles.com/packages/lf20_1Lckxtas.json")

with st.container():
    left_column,right_column = st.columns(2)
    with left_column:
        type = st.selectbox("Select Type: ",["None","CASH_IN","CASH_OUT","DEBIT","PAYMENT","TRANSFER"])
        if type == "CASH_IN":
            lis = [1,0,0,0,0]
        elif type =="CASH_OUT":lis = [0,1,0,0,0]
        elif type =="DEBIT" : lis = [0,0,1,0,0]
        elif type == "PAYMENT" : lis = [0,0,0,1,0]
        else : lis = [0,0,0,0,1]

        amount = st.number_input(label = "ENTER AMOUNT",step = 1., format = "%.2f")
        oldBalanceOrigin = st.number_input(label = "Enter old balance origin",step = 1., format = "%.2f")
        newBalanceOrigin = st.number_input(label = "Enter new balance origin",step = 1., format = "%.2f")
        isFlaggedFraud = st.number_input(label = "Enter isflaggedfraud",step = 1., format = "%.2f")

        lis.extend([amount, oldBalanceOrig, newBalanceOrig, isFlaggedFraud])

        with right_column:
            st.lottie(topProduct, height=600, key="topProduct")

if st.button("Predict"):
    # Check if all values are entered
    if type != "None" and amount != 0.0 and oldBalanceOrig != 0.0 and newBalanceOrig != 0.0:
        # Load selected model
        choice = st.selectbox("Select Model", ["LOGISTIC", "Decision Trees", "SVM"])
        if choice == "LOGISTIC":
            loaded_model = pickle.load(open('logistic_model.sav', 'rb'))
        elif choice == "Decision Trees":
            loaded_model = pickle.load(open('decision_model.sav', 'rb'))
        elif choice == "SVM":
            loaded_model = pickle.load(open('svm_model.sav', 'rb'))
        else:
            st.write("Invalid Model Selection")

        # Predict
        pred = loaded_model.predict([lis])
        if pred[0] == 1:
            st.subheader("Fraud Transaction")
        else:
            st.subheader("Not a Fraud Transaction")
    else:
        st.write("Please enter all values")
