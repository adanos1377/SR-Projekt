import pickle
import pandas as pd
import os

class partners_data_splitter:
    def __init__(self,path,nrows=None,dtypes=None):
        self.path=path
        self.nrows=nrows
        self.header_info=['Sale','SalesAmountInEuro','time_delay_for_conversion','click_timestamp','nb_clicks_1week','product_price','product_age_group','device_type','audience_id','product_gender',
                          'product_brand','product_category_1','product_category_2','product_category_3','product_category_4','product_category_5','product_category_6','product_category_7',
                          'product_country','product_id','product_title','partner_id','user_id']
    def product_factors(self,df):
        if(df.shape[0]>0):
            temp_total_sales_df=df[df["Sale"]==1]
            total_sales=temp_total_sales_df["SalesAmountInEuro"].sum()
            number_of_clicks=df.shape[0]
        else:
            total_sales=0.0
            number_of_clicks=0.0
        temp_product_factors={}
        temp_product_factors["Total_Sales"]=total_sales
        temp_product_factors["Number_Of_Clicks"]=number_of_clicks
        return temp_product_factors
    def partner_day_factors(self, df_partner_day):
        per_partner_factors_for_day={}
        temp_df=df_partner_day.groupby("product_id")
        for product_id, df_day_product in temp_df:
            temp_product_factors=self.product_factors(df_day_product)
            per_partner_factors_for_day[product_id]=temp_product_factors
        return per_partner_factors_for_day

    def get_split_chrono(self):
        self.read_file()
        list_of_dfs={}
        partners_selected_for_test_parameter_for_Mr_Riegel_20201103 =["C0F515F0A2D0A5D9F854008BA76EB537", "E3DDEB04F8AFF944B11943BB57D2F620",
         "E68029E9BCE099A60571AF757CBB6A08"]
        self.df["date"] = self.df['click_timestamp'].apply(lambda x: str(pd.to_datetime(int(x), unit='s').date()))
        self.df.sort_values(["date"], ascending=True, inplace=True)
        print(self.df.dtypes)
        df_groups_for_partners =self.df.groupby("partner_id")
        for partner_id, df_group_for_partner in df_groups_for_partners:
            if partner_id in partners_selected_for_test_parameter_for_Mr_Riegel_20201103:
                test_parameter_for_Mr_Riegel_20201103 = df_group_for_partner.shape[0]
                print("test_parameter_for_Mr_Riegel_20201103 for partner_id " + partner_id + " :", test_parameter_for_Mr_Riegel_20201103)
            p = os.path.join(os.getcwd(), "data_{}.csv".format(partner_id.lower()))
            df_group_for_partner.to_csv(p, index=False)
            temp_df=pd.DataFrame(df_group_for_partner)
            #temp_df["date"]=temp_df['click_timestamp'].apply(lambda x:str(pd.to_datetime(int(x),unit='s').date()))
            df_group_days=temp_df.groupby("date")
            list_of_dfs[partner_id]={}
            for day, df_group_day in df_group_days:
                temp_dict=pd.DataFrame(df_group_day)
                per_partner_factors_for_day=self.partner_day_factors(temp_dict)
                list_of_dfs[partner_id][day]={"df_data":temp_dict,"factors_data":per_partner_factors_for_day}
        self.list_of_dfs=list_of_dfs

    def read_file(self):
        self.df=pd.read_csv(self.path,sep="\t",nrows=self.nrows,header=None,names=self.header_info) #,dtype=self.dtypes
        #print(self.df.dtypes)
    def pickle(self):
        pickle.dump(self.list_of_dfs,open("split_data_chrono.ckl","xb"))


if __name__ == '__main__':
    path = "E:\Criteo_Conversion_Search\CriteoSearchData"
    splitter=partners_data_splitter(path,1000,None)
    splitter.get_split_chrono() #podział na pomniejsze pliki według daty
    data=splitter.list_of_dfs #pobranie powyższego wyniku z pola klasy
    #splitter.pickle()
