import pickle
import numpy as np
from flask import Flask, request, jsonify, render_template
import logging
from pyspark.mllib.recommendation import ALS, MatrixFactorizationModel
from app_api import make_n_recommendation_low_cust, make_n_recommendation_mid_cust, make_n_recommendation_high_cust, determine_user
with open('data/pdt_cat_names.pkl', 'rb') as read_file:
    pdt_cat_names = pickle.load(read_file)

# with open('data/pdt_cat_names.pkl', 'rb') as read_file:
#     pdt_cat_names = pickle.load(read_file)
# with open('data/low_value_num_cust_id.pkl', 'rb') as read_file:
#     low_value_num_cust_id = pickle.load(read_file)
# with open('data/mid_value_num_cust_id.pkl', 'rb') as read_file:
#     mid_value_num_cust_id = pickle.load(read_file)
# with open('data/high_value_num_cust_id.pkl', 'rb') as read_file:
#     high_value_num_cust_id = pickle.load(read_file)

# with open('models/pdt_cat_cold_start.pkl', 'rb') as read_file:
#     pdt_cat_cold_start = pickle.load(read_file)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('index.html')
    if flask.request.method == 'POST':
        # Extract the input
        user_id = flask.request.form['user']


# @app.route('/recommendations_new', methods=['GET', 'POST'])
# def recommendations_new():
#     # Grab and save query parameters # 
#     if request.method == 'GET':
#         top_N_for_new_cust = int(request.args.get("N_reco"))
#         new_cust_recommendations = new_cust_most_pop.getRec(top_N_for_new_cust)
#         new_cust_most_pop.reset()

#         return render_template('recommendations_new.html', new_cust_recommendations=new_cust_recommendations)

@app.route('/recommendations_existing', methods=['GET', 'POST'])
def recommendations_existing():
    # Grab and save query parameters # 
    userID = 0 
    selected = ['furniture_deco']
    if request.method == 'GET':
        if request.args.get("user_id") != None:
            userID1 = int(request.args.get("user_id"))
            userID = userID1
            print("YOYO")
            selected = request.args.get("selected_categories")
        recommends = determine_user(userID, selected)

        return render_template('recommendations_existing.html', existing_cust_recommendations=recommends, pdt_cat_names=pdt_cat_names)



if __name__=="__main__":
    app.run(debug=True)