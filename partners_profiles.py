import os
import pandas as pd
import pickle

class partners_profiles:
    def __init__(self,partners_ids,cost):
        self.partners=partners_ids
        self.cost=cost
        self.header_info = ['Sale', 'SalesAmountInEuro', 'time_delay_for_conversion', 'click_timestamp', 'nb_clicks_1week',
                       'product_price', 'product_age_group', 'device_type', 'audience_id', 'product_gender',
                       'product_brand', 'product_category_1', 'product_category_2', 'product_category_3',
                       'product_category_4', 'product_category_5', 'product_category_6', 'product_category_7',
                       'product_country', 'product_id', 'product_title', 'partner_id', 'user_id']

    def read_partners_profiles(self):
        loaded=self.load_click_costs()
        click_costs_dict={}
        for id in self.partners:
            if id not in loaded:
                click_cost=self.calculate_click_cost(id)
                click_costs_dict[id]=click_cost
                loaded[id]=click_cost
            else:
                click_costs_dict[id]=loaded[id]
        with open('click_costs.pickle', 'wb') as handle:
            pickle.dump(loaded, handle, protocol=pickle.HIGHEST_PROTOCOL)
        return click_costs_dict
    def calculate_click_cost(self,id):
        p = os.path.join(os.getcwd(), "splitted data\data_{}.csv".format(id.lower()))
        df = pd.read_csv(p,low_memory=False)
        if (df.shape[0] > 0):
            temp_total_sales_df = df[df['Sale'] == 1]
            total_sales = temp_total_sales_df["SalesAmountInEuro"].sum()
            number_of_clicks = df.shape[0]
            click_cost=(total_sales*self.cost)/number_of_clicks
        else:
            click_cost=0
        return round(click_cost,4)
    def load_click_costs(self):
        with open('click_costs.pickle', 'rb') as handle:
            return pickle.load(handle)