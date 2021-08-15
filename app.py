from flask import Flask, render_template, request
from sklearn.tree import DecisionTreeRegressor
import pickle
import numpy as np
import pandas as pd
from joblib import dump, load

app = Flask(__name__)

model = load(open("svm_model_linear.pkl", "rb"))
model2 = load(open("random_forest_model.pkl", "rb"))
app.secret_key = "abfdhsuadhsaujc"  

######################
data=pd.read_csv('cpdata.csv')
label= pd.get_dummies(data.label).iloc[: , 1:]
data= pd.concat([data,label],axis=1)
data.drop('label', axis=1,inplace=True)
data_copy = data
######################


@app.route("/",methods=["POST", "GET"])
def intial_route():
    
    return render_template('index.html',crop = 'None')

@app.route("/index_fert",methods=["POST", "GET"])
def index_fert():
    
    return render_template('index2.html',fert_type = 'None')

@app.route("/results_crop", methods=["POST", "GET"])
def results_crop():
    result = request.form
    print(request.form)
    rainfall = float(result["rainfall"])
    humidity = float(result["humidity"])
    ph = float(result["ph"])
    temperature = float(result['temperature'])

    #check parameters order
    prediction = model.predict([[temperature,humidity,ph,rainfall]])
    
    return render_template('index.html',crop = prediction[0])

@app.route("/index_crop", methods=["POST", "GET"])
def index_crop():
    return
@app.route("/results_fertilizer", methods=["POST", "GET"])
def results_fertilizer():
    result = request.form
    print(request.form)
    ca = float(result["ca"])
    mg = float(result["mg"])
    k = float(result["k"])
    s = float(result["s"])
    n = float(result["n"])
    lime = float(result["lime"])
    c = float(result["c"])
    p = float(result["p"])
    moisture = float(result["moisture"])

    #check parameters order
    prediction = model2.predict([[ca,mg,k,s,n,lime,c,p,moisture]])[0]
    if prediction == 1:
        fert_type = 'Organic and Inorganic Fertilizer'
    elif prediction == 2:
       fert_type = 'Nitrogen Fertilizer'
    elif prediction == 3:
       fert_type = 'Phosphate Fertilizer'
    elif prediction == 4:
        fert_type = 'Potassium Fertilizer'

    return render_template('index2.html', fert_type = fert_type)


if __name__ == "__main__":
    app.run()