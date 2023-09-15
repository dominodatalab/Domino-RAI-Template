import pickle
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from domino_data_capture.data_capture_client import DataCaptureClient
import datetime
import uuid
 
feature_names = ["age", "workclass", "fnlwgt", "education", "education-num", "marital-status", "occupation", "relationship", "race", "gender", "capital-gain", "capital-loss", "hours-per-week", "native-country"]
predict_names = ['income']
pred_client = DataCaptureClient(feature_names, predict_names)
 
 
with open("../artifacts/model.bin", 'rb') as f_in:
    loaded_model = pickle.load(f_in)
    f_in.close()  # close the file 
 
def predict(age, workclass, fnlwgt, education, education_num, marital_status, occupation, relationship, race, gender, capital_gain, capital_loss, hours_per_week, native_country, census_id=None):
    transformed_data = pd.DataFrame([[age, workclass, fnlwgt, education, education_num, marital_status, occupation, relationship, race, gender, capital_gain, capital_loss, hours_per_week, native_country]],columns=["age", "workclass", "fnlwgt", "education", "education-num", "marital-status", "occupation", "relationship", "race", "gender", "capital-gain", "capital-loss", "hours-per-week", "native-country"])
    prediction = loaded_model.predict(transformed_data)
    
    if census_id is None:
        print(f"No Customer ID found! Creating a new one.")
        census_id = str(uuid.uuid4())
    
    feature_array = list([age, workclass, fnlwgt, education, education_num, marital_status, occupation, relationship, race, gender, capital_gain, capital_loss, hours_per_week, native_country])
    pred_array = list(prediction)
    
    pred_client.capturePrediction(feature_array, prediction, event_id=census_id)
    
    return dict(prediction=prediction[0])