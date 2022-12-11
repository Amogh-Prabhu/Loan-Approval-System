import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

app = Flask(__name__)

df =  {
    "ApplicantIncome": 0,
    "CoapplicantIncome": 0,
    "LoanAmount": 0,
    "Loan_Amount_Term": 0,
    "Credit_History": 0,
    "Gender_Male": 0,
    "Married_Yes": 0,
    "Dependents_1": 0,
    "Dependents_2": 0,
    "Dependents_3+": 0,
    "Education_Not Graduate": 0,
    "Self_Employed_Yes": 0,
    "Property_Area_Semiurban": 0,
    "Property_Area_Urban": 0,
}
loan_amount = 0
normalMin = pd.DataFrame(pd.read_csv("./data/normalmin.csv"))
normalMax = pd.DataFrame(pd.read_csv("./data/normalmax.csv"))
model = keras.models.load_model("./model.h5")

@app.route("/")
def index():
    return render_template("./index.html")

@app.route("/userdetails",methods=['GET','POST'])
def userdetails():
    if request.method == 'POST':
        if request.form["gender"] == "Male":
            df["Gender_Male"] = 1
        if request.form["marriage"] == "Yes":
            df["Married_Yes"] = 1
        if request.form["nod"] == '1':
            df["Dependents_1"] = 1
        elif request.form["nod"] == '2':
            df["Dependents_2"] = 1
        elif request.form["nod"] != '0':
            df["Dependents_3+"] = 1
        if request.form["graduation"] == "Not-Graduate":
            df["Education_Not Graduate"] = 1
        if request.form["self-emp"] == "Employed":
            df["Self_Employed_Yes"] = 1
        if request.form["PA"] == "Urban":
            df["Property_Area_Urban"] = 1
        elif request.form["PA"] == "Semi-Urban":
            df["Property_Area_Semiurban"] = 1
        return redirect(url_for('moneydetails'))
    return "Hello World"

@app.route("/moneydetails",methods=['GET','POST'])
def moneydetails():
    global loan_amount
    if request.method == 'POST':
        df["ApplicantIncome"] = int(request.form["ApplicantIncome"])
        df["LoanAmount"] = int(request.form["LoanAmount"])
        df["Loan_Amount_Term"] = int(request.form["Loan_Amount_Term"])
        df["Credit_History"] = int(request.form["Credit_History"])
        loan_amount = df["LoanAmount"]
        return redirect(url_for('prediction'))
    return render_template("./moneydetails.html")

@app.route("/prediction")
def prediction():
    global df
    for key in df.keys():
        df[key] = (df[key]-normalMin[key])/(normalMax[key]-normalMin[key])
    predict = model.predict(pd.DataFrame(df))
    chances = round(predict[0][0]*10000)/100
    df =  {
        "ApplicantIncome": 0,
        "CoapplicantIncome": 0,
        "LoanAmount": 0,
        "Loan_Amount_Term": 0,
        "Credit_History": 0,
        "Gender_Male": 0,
        "Married_Yes": 0,
        "Dependents_1": 0,
        "Dependents_2": 0,
        "Dependents_3+": 0,
        "Education_Not Graduate": 0,
        "Self_Employed_Yes": 0,
        "Property_Area_Semiurban": 0,
        "Property_Area_Urban": 0,
    }
    if chances>=50:
        return render_template("./prediction.html",data=chances,color="darkgreen")
    else:
        return render_template("./prediction.html",data=chances,color="darkred")

@app.route("/recommendation")
def recommend():
    print(loan_amount)
    return render_template("./recommendation.html",LA=loan_amount)

app.run(debug=True)
