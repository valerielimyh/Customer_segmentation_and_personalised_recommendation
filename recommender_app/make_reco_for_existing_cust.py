from pyspark.mllib.recommendation import ALS, MatrixFactorizationModel
def get_product_cat_num(pdt_cat, fav_pdt_cat_list):
    """
    return all product_cat_num(s) of user's favorite pdt_cat
    
    Parameters
    ----------
    pdt_cat: spark Dataframe, pdt_cat data
    
    fav_pdt_cat_list: list, user's list of favorite pdt_cat
    
    Return
    ------
    product_cat_num_list: list of product_cat_num(s)
    """
    product_cat_num_list = []
    for pdt_category in fav_pdt_cat_list:
        product_cat_nums = pdt_cat \
            .filter(pdt_cat.product_category_name_english.like('%{}%'.format(pdt_category))) \
            .select('product_cat_num') \
            .rdd \
            .map(lambda r: r[0]) \
            .collect()
        product_cat_num_list.extend(product_cat_nums)
    return list(set(product_cat_num_list))

def add_new_user_to_data(train_data, product_cat_num_list, spark_context):
    """
    add new rows with new user, user's pdt_cat and ratings to
    existing train data

    Parameters
    ----------
    train_data: spark RDD, ratings data
    
    product_cat_num_list: list, list of product_cat_num(s)

    spark_context: Spark Context object
    
    Return
    ------
    new train data with the new user's rows
    """
    # get new user id
    new_id = train_data.map(lambda r: r[0]).max() + 1
    # get max rating
    max_rating = train_data.map(lambda r: r[2]).max()
    # create new user rdd
    user_rows = [(new_id, product_cat_num, max_rating) for product_cat_num in product_cat_num_list]
    new_rdd = spark_context.parallelize(user_rows)
    # return new train data
    return train_data.union(new_rdd)

def get_inference_data(train_data, pdt_cat, product_cat_num_list):
    """
    return a rdd with the userid and all pdt_cat (except ones in product_cat_num_list)

    Parameters
    ----------
    train_data: spark RDD, ratings data

    pdt_cat: spark Dataframe, pdt_cat data
    
    product_cat_num_list: list, list of product_cat_num(s)

    Return
    ------
    inference data: Spark RDD
    """
    # get new user id
    new_id = train_data.map(lambda r: r[0]).max() + 1
    # return inference rdd
    return pdt_cat.rdd \
        .map(lambda r: r[0]) \
        .distinct() \
        .filter(lambda x: x not in product_cat_num_list) \
        .map(lambda x: (new_id, x))

def make_recommendation(best_model_params, ratings_data, pdt_cat, 
                        fav_pdt_cat_list, n_recommendations, spark_context):
    """
    return top n pdt_cat recommendation based on user's input list of favorite pdt_cat


    Parameters
    ----------
    best_model_params: dict, {'iterations': iter, 'rank': rank, 'lambda_': reg}

    ratings_data: spark RDD, ratings data

    pdt_cat: spark Dataframe, pdt_cat data

    fav_pdt_cat_list: list, user's list of favorite pdt_cat

    n_recommendations: int, top n recommendations

    spark_context: Spark Context object

    Return
    ------
    list of top n pdt_cat recommendations
    """
    # modify train data by adding new user's rows
    product_cat_num_list = get_product_cat_num(pdt_cat, fav_pdt_cat_list)
    train_data = add_new_user_to_data(ratings_data, product_cat_num_list, spark_context)
    
    # train best ALS
    model = ALS.train(
        ratings=train_data,
        iterations=best_model_params.get('iterations', None),
        rank=best_model_params.get('rank', None),
        lambda_=best_model_params.get('lambda_', None),
        seed=99)
    
    # get inference rdd
    inference_rdd = get_inference_data(ratings_data, pdt_cat, product_cat_num_list)
    print(inference_rdd.take(10))
    # inference
    predictions = model.predictAll(inference_rdd).map(lambda r: (r[1], r[2]))
    
    # get top n product_cat_num
    topn_rows = predictions.sortBy(lambda r: r[1], ascending=False).take(n_recommendations)
    topn_ids = [r[0] for r in topn_rows]
    
    # return pdt_cat titles
    return pdt_cat.filter(pdt_cat.product_cat_num.isin(topn_ids)) \
                    .select('product_category_name_english') \
                    .rdd \
                    .map(lambda r: r[0]) \
                    .collect()