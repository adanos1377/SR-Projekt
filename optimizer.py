import random
import sys


class optimizer:
    def __init__(self,seed,how_many,id):
        self.products=[]
        self.seed=seed
        self.how_many=how_many
        self.data=None
        self.id=id
        self.excluded_products=[]

    def get_excluded_products_pseudorandomly(self):
        dummy_list_of_potentially_excluded_products = self.products
        dummy_list_of_potentially_excluded_products.sort()
        dummy_how_many_products = round(len(dummy_list_of_potentially_excluded_products)/self.how_many)
        random.seed(self.seed)
        excluded_products = random.sample(dummy_list_of_potentially_excluded_products, dummy_how_many_products)
        return excluded_products
    def next_day(self,data,day):
        SoFar = self.products
        if self.data is None:
            self.data=data
        else:
            self.data=self.data.append(data,ignore_index=True)
        self.products = self.__get_products_seen_today(self.data)
        orig_stdout = sys.stdout
        sys.stdout = open("exclusion_log.txt", "a")
        print('number of all products: ',len(self.products))
        sys.stdout.close()
        sys.stdout=orig_stdout
        self.excluded_products=self.get_excluded_products_pseudorandomly()
        return self.excluded_products, SoFar
    def __get_products_seen_today(self,data_df):
        return data_df['product_id'].unique().tolist()
