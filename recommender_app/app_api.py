import pickle
# from flask_bootstrap import Bootstrap 
from flask import Flask, request, jsonify, render_template
from make_reco_for_existing_cust import *
from make_reco_for_new_cust import Recommender

# spark imports
from pyspark.sql import SparkSession
from pyspark.mllib.recommendation import ALS, MatrixFactorizationModel


# spark config
spark = SparkSession \
    .builder \
    .appName("low value cust pdt category recommendation") \
    .config("spark.driver.maxResultSize", "96g") \
    .config("spark.driver.memory", "96g") \
    .config("spark.executor.memory", "8g") \
    .config("spark.master", "local[12]") \
    .getOrCreate()
# get spark context
sc = spark.sparkContext

pdt_cat = spark.read.load('data/pdt_cat.csv', format='csv', header=True, inferSchema=True)

with open('data/pdt_cat_names.pkl', 'rb') as read_file:
    pdt_cat_names = pickle.load(read_file)
with open('data/low_value_num_cust_id.pkl', 'rb') as read_file:
    low_value_num_cust_id = pickle.load(read_file)
with open('data/mid_value_num_cust_id.pkl', 'rb') as read_file:
    mid_value_num_cust_id = pickle.load(read_file)
with open('data/high_value_num_cust_id.pkl', 'rb') as read_file:
    high_value_num_cust_id = pickle.load(read_file)
high_cust_model = MatrixFactorizationModel.load(sc, "models/spark_als_high_value_cust_model.model")
mid_cust_model = MatrixFactorizationModel.load(sc, "models/spark_als_mid_value_cust_model.model")
low_cust_model = MatrixFactorizationModel.load(sc, "models/spark_als_low_value_cust_model.model")
with open('models/pdt_cat_cold_start.pkl', 'rb') as read_file:
    pdt_cat_cold_start = pickle.load(read_file)

# get recommends for new customer

new_cust_most_pop = Recommender(pdt_cat_cold_start, most_popular=True)

pdt_cat = spark.read.load('data/pdt_cat.csv', format='csv', header=True, inferSchema=True)

high_cust_rating = sc.textFile('data/high_value_cust_num_pdt_rating_reco.csv')
# preprocess data -- only need ['customer_id,product_category_name_english,review_score']
high_custheader = high_cust_rating.take(1)[0]
high_cust_rating_data = high_cust_rating \
    .filter(lambda line: line!=high_custheader) \
    .map(lambda line: line.split(",")) \
    .map(lambda tokens: (int(tokens[0]), int(tokens[1]), float(tokens[2]))) \
    .cache()

mid_cust_rating = sc.textFile('data/mid_value_cust_num_pdt_rating_reco.csv')
# preprocess data -- only need ['customer_id,product_category_name_english,review_score']
mid_custheader = mid_cust_rating.take(1)[0]
mid_cust_rating_data = mid_cust_rating \
    .filter(lambda line: line!=mid_custheader) \
    .map(lambda line: line.split(",")) \
    .map(lambda tokens: (int(tokens[0]), int(tokens[1]), float(tokens[2]))) \
    .cache()

low_cust_rating = sc.textFile('data/low_value_cust_num_pdt_rating_reco.csv')
# preprocess data -- only need ['customer_id,product_category_name_english,review_score']
low_custheader = low_cust_rating.take(1)[0]
low_cust_rating_data = low_cust_rating \
    .filter(lambda line: line!=low_custheader) \
    .map(lambda line: line.split(",")) \
    .map(lambda tokens: (int(tokens[0]), int(tokens[1]), float(tokens[2]))) \
    .cache()

# get recommends for existing customer
def determine_user(userID, selected):
    if userID in low_value_num_cust_id:
        pdt_category_reco_low_cust = make_n_recommendation_low_cust(selected)
        return pdt_category_reco_low_cust

    elif userID in mid_value_num_cust_id:
        pdt_category_reco_mid_cust = make_n_recommendation_mid_cust(selected)
        return pdt_category_reco_mid_cust
    else:
        pdt_category_reco_high_cust = make_n_recommendation_high_cust(selected)
        return pdt_category_reco_high_cust


def make_n_recommendation_low_cust(my_favorite_pdt_cat):
    low_cust_recommends = make_recommendation(
    best_model_params={'iterations': 10, 'rank': 20, 'lambda_': 0.1}, 
    ratings_data=low_cust_rating_data, 
    pdt_cat=pdt_cat, 
    fav_pdt_cat_list=my_favorite_pdt_cat, 
    n_recommendations=10, 
    spark_context=sc)
    return low_cust_recommends

def make_n_recommendation_mid_cust(my_favorite_pdt_cat):
    mid_cust_recommends = make_recommendation(
    best_model_params={'iterations': 10, 'rank': 12, 'lambda_': 0.1}, 
    ratings_data=mid_cust_rating_data, 
    pdt_cat=pdt_cat, 
    fav_pdt_cat_list=my_favorite_pdt_cat, 
    n_recommendations=10, 
    spark_context=sc)
    return mid_cust_recommends


def make_n_recommendation_high_cust(my_favorite_pdt_cat):
    high_cust_recommends = make_recommendation(
    best_model_params={'iterations': 10, 'rank': 8, 'lambda_': 0.05}, 
    ratings_data=high_cust_rating_data, 
    pdt_cat=pdt_cat, 
    fav_pdt_cat_list=my_favorite_pdt_cat, 
    n_recommendations=10, 
    spark_context=sc)
    
    return high_cust_recommends
