from flask import Flask, render_template, url_for, request
import pandas as pd
import numpy as np
import pickle
import sklearn
app= Flask(__name__)
model_file= open('rf.pkl','rb')
model=pickle.load(model_file) 

@app.route('/')
def welcome():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict_price():
    Diesel=0
    if request.method=='POST':
        year_old= int(request.form['year_old'])
        Present_Price= float(request.form['Present_Price'])
        Kms_Driven= int(request.form['Kms_Driven'])
        Owner=int(request.form['Owner'])
        Petrol=request.form['Petrol']
        if Petrol=='Petrol':
            Petrol=1
            Diesel=0
        elif Petrol=='Diesel':
            Petrol=0
            Diesel=1
        else:
            Petrol=0
            Diesel=0
        Individual= request.form['Individual']
        if Individual=='Individual':
            Individual=1
        else:
            Individual=0
        year_old=2020-year_old
        Manual=request.form['Manual']
        if Manual=='Manual':
            Manual=1
        else:
            Manual=0
        ypred=model.predict([[Present_Price, Kms_Driven,Owner,year_old,Diesel,Petrol,Individual,Manual]])
        if ypred<0:
            return render_template('index.html', prediction_text="Sorry, you cant sell this car")
        else:
            return render_template('index.html' , prediction_text="Your car can be sold at the price of Rs {}".format(ypred))
    else:
        return render_template('index.html')

if __name__=='__main__':
    app.run(debug=True)
    