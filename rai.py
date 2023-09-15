import zipfile

from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

import pandas as pd
from lightgbm import LGBMClassifier

from raiutils.dataset import fetch_dataset
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

def split_label(dataset, target_feature):
    X = dataset.drop([target_feature], axis=1)
    y = dataset[[target_feature]]
    return X, y

def create_classification_pipeline(X):
    pipe_cfg = {
        'num_cols': X.dtypes[X.dtypes == 'int64'].index.values.tolist(),
        'cat_cols': X.dtypes[X.dtypes == 'object'].index.values.tolist(),
    }
    num_pipe = Pipeline([
        ('num_imputer', SimpleImputer(strategy='median')),
        ('num_scaler', StandardScaler())
    ])
    cat_pipe = Pipeline([
        ('cat_imputer', SimpleImputer(strategy='constant', fill_value='?')),
        ('cat_encoder', OneHotEncoder(handle_unknown='ignore', sparse=False))
    ])
    feat_pipe = ColumnTransformer([
        ('num_pipe', num_pipe, pipe_cfg['num_cols']),
        ('cat_pipe', cat_pipe, pipe_cfg['cat_cols'])
    ])

    # Append classifier to preprocessing pipeline.
    # Now we have a full prediction pipeline.
    pipeline = Pipeline(steps=[('preprocessor', feat_pipe),
                               ('model', LGBMClassifier(random_state=0))])

    return pipeline

outdirname = 'responsibleai.12.28.21'
zipfilename = outdirname + '.zip'

print("Fetching dataset.")
fetch_dataset('https://publictestdatasets.blob.core.windows.net/data/' + zipfilename, zipfilename)

print("Unzipping.")
with zipfile.ZipFile(zipfilename, 'r') as unzip:
    print(f"Unzipping {zipfilename}...")
    unzip.extractall('.')


target_feature = 'income'
categorical_features = ['workclass', 'education', 'marital-status',
                        'occupation', 'relationship', 'race', 'gender', 'native-country']

print("Reading into dataframes.")
train_data = pd.read_csv('adult-train.csv', skipinitialspace=True)
test_data = pd.read_csv('adult-test.csv', skipinitialspace=True)

print("Creating training pipeline.")
X_train_original, y_train = split_label(train_data, target_feature)
X_test_original, y_test = split_label(test_data, target_feature)

pipeline = create_classification_pipeline(X_train_original)

y_train = y_train[target_feature].to_numpy()
y_test = y_test[target_feature].to_numpy()

# REDUCING THIS FROM 500 TO 50
# Take 500 samples from the test data
test_data_sample = test_data.sample(n=50, random_state=5)

print("Training...")
model = pipeline.fit(X_train_original, y_train)


################
print("Creating insights dashboard")

from raiwidgets import ResponsibleAIDashboard
from responsibleai import RAIInsights

###############
target_feature = 'income'
categorical_features = ['workclass', 'education', 'marital-status',
                        'occupation', 'relationship', 'race', 'gender', 'native-country']

from responsibleai.feature_metadata import FeatureMetadata
feature_metadata = FeatureMetadata(categorical_features=categorical_features, dropped_features=[])
################
rai_insights = RAIInsights(model, train_data, test_data_sample, target_feature, 'classification',
                           feature_metadata=feature_metadata)
                           
###############

# Interpretability
rai_insights.explainer.add()
# Error Analysis
#rai_insights.error_analysis.add()
# Counterfactuals: accepts total number of counterfactuals to generate, the label that they should have, and a list of 
                # strings of categorical feature names
rai_insights.counterfactual.add(total_CFs=10, desired_class='opposite')

##################################
### THIS WILL TAKE A LONG TIME:
##################################

print("Computing...")
rai_insights.compute()
print("Computed.")

##################################

print("Preparing cohort list")
from raiutils.cohort import Cohort, CohortFilter, CohortFilterMethods

# Cohort on age and hours-per-week features in the dataset
cohort_filter_age = CohortFilter(
    method=CohortFilterMethods.METHOD_LESS,
    arg=[65],
    column='age')
cohort_filter_hours_per_week = CohortFilter(
    method=CohortFilterMethods.METHOD_GREATER,
    arg=[40],
    column='hours-per-week')

user_cohort_age_and_hours_per_week = Cohort(name='Cohort Age and Hours-Per-Week')
user_cohort_age_and_hours_per_week.add_cohort_filter(cohort_filter_age)
user_cohort_age_and_hours_per_week.add_cohort_filter(cohort_filter_hours_per_week)

# Cohort on marital-status feature in the dataset
cohort_filter_marital_status = CohortFilter(
    method=CohortFilterMethods.METHOD_INCLUDES,
    arg=["Never-married", "Divorced"],
    column='marital-status')

user_cohort_marital_status = Cohort(name='Cohort Marital-Status')
user_cohort_marital_status.add_cohort_filter(cohort_filter_marital_status)

# Cohort on index of the row in the dataset
cohort_filter_index = CohortFilter(
    method=CohortFilterMethods.METHOD_LESS,
    arg=[20],
    column='Index')

user_cohort_index = Cohort(name='Cohort Index')
user_cohort_index.add_cohort_filter(cohort_filter_index)

# Cohort on predicted target value
cohort_filter_predicted_y = CohortFilter(
    method=CohortFilterMethods.METHOD_INCLUDES,
    arg=['>50K'],
    column='Predicted Y')

user_cohort_predicted_y = Cohort(name='Cohort Predicted Y')
user_cohort_predicted_y.add_cohort_filter(cohort_filter_predicted_y)

# Cohort on predicted target value
cohort_filter_true_y = CohortFilter(
    method=CohortFilterMethods.METHOD_INCLUDES,
    arg=['>50K'],
    column='True Y')

user_cohort_true_y = Cohort(name='Cohort True Y')
user_cohort_true_y.add_cohort_filter(cohort_filter_true_y)

cohort_list = [user_cohort_age_and_hours_per_week,
               user_cohort_marital_status,
               user_cohort_index,
               user_cohort_predicted_y,
               user_cohort_true_y]
               
               
################################

print("Monkey-patching environment")

from flask_cors import CORS
from rai_core_flask.environments.base_environment import BaseEnvironment
 
class DominoAppEnvironment(BaseEnvironment):
    def __init__(self, service):
        self.successfully_detected = True
        self.base_url = "./.."
        print(f"Monkey-patching base url to: {self.base_url}")

    def select(self, service):
        service.with_credentials = False
        service.cors = CORS(service.app)
        service.env_name = 'domino_app'
 
def domino_build_environment(service):
    print("Monkey-patched build environment.")
    domino_env = DominoAppEnvironment(service)
    domino_env.select(service)
    return domino_env

from rai_core_flask import environment_detector, flask_helper
#environment_detector.build_environment = domino_build_environment
#flask_helper.build_environment = domino_build_environment

################################

print("Starting dashboard")
a=ResponsibleAIDashboard(rai_insights, cohort_list=cohort_list, public_ip="0.0.0.0", port=8888)
print("Started dashboard.")

###############################

import subprocess

# This is a sample Python/Flask app showing Domino's App publishing functionality.
# You can publish an app by clicking on "Publish" and selecting "App" in your
# quick-start project.

import json
import flask
from flask import request, redirect, url_for
import numpy as np

class ReverseProxied(object):
  def __init__(self, app):
      self.app = app
  def __call__(self, environ, start_response):
      script_name = environ.get('HTTP_X_SCRIPT_NAME', '')
      if script_name:
          environ['SCRIPT_NAME'] = script_name
          path_info = environ['PATH_INFO']
          if path_info.startswith(script_name):
              environ['PATH_INFO'] = path_info[len(script_name):]
      # Setting wsgi.url_scheme from Headers set by proxy before app
      scheme = environ.get('HTTP_X_SCHEME', 'https')
      if scheme:
        environ['wsgi.url_scheme'] = scheme
      # Setting HTTP_HOST from Headers set by proxy before app
      remote_host = environ.get('HTTP_X_FORWARDED_HOST', '')
      remote_port = environ.get('HTTP_X_FORWARDED_PORT', '')
      if remote_host and remote_port:
          environ['HTTP_HOST'] = f'{remote_host}:{remote_port}'
      return self.app(environ, start_response)
      
#####################
print("Attaching reverse proxy.")
a._service.app.wsgi_app = ReverseProxied(a._service.app.wsgi_app)
print("Reverse proxy installed.")

import time
while True:
    time.sleep(1)
print("BREAK!")