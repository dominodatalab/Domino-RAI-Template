#!/usr/bin/env bash

# Examples
# Choose 1 to uncomment and insert your actual app file name.

## Flask example
# export LC_ALL=C.UTF-8
# export LANG=C.UTF-8
# export FLASK_APP=app-flask.py
# export FLASK_DEBUG=1
# python -m flask run --host=0.0.0.0 --port=8888

python rai.py

## Dash Example
#python app-dash.py

## R/Shiny Example
#R -e 'shiny::runApp("./", port=8888, host="0.0.0.0")'