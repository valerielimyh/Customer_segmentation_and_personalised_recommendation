class Recommender():
    def __init__(self, table, most_popular=False):
        """
        Class to create a movie recommender
        Arguments
        - table        : dataframe of pdt_cat with global_avg stats
        - most_popular : sort the recommendations by most popular
        """
        if (most_popular == False):
            self.table = table.sort_values(by=['global_avg', 'rating_cnt'], ascending=[False, False])
        else:
            table['popular_rating'] = (table['global_avg'] - 3) * table['rating_cnt']
            self.table = table.sort_values(by=['popular_rating', 'rating_cnt'], ascending=[False, False])

    def getRec(self, N):
        """
        Return the names of N product categories with the greatest global average rating 
        that has not been recommended yet
        """
        for row in self.table.itertuples():
            if row.recommended == 0:
                ID = pdt_cat['product_cat_num'].iloc[:N].values
                self.table.loc[self.table.index[self.table['product_cat_num'].isin(ID)], 'recommended'] = 1
                return pdt_cat['product_category_name_english'].iloc[:N].values.tolist()
        
    def reset(self):
        """
        Reset recommender memory, so that all pdt_cat are listed as unrecommended
        """
        self.table['recommended'] = 0