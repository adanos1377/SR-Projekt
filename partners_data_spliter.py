import os
import pandas as pd
import datetime
import pickle

class partners_data_splitter:
    def __init__(self,path,nrows=None,dtypes=None):
        self.path=path
        self.nrows=nrows
        self.header_info=['Sale','SalesAmountInEuro','time_delay_for_conversion','click_timestamp','nb_clicks_1week','product_price','product_age_group','device_type','audience_id','product_gender',
                          'product_brand','product_category_1','product_category_2','product_category_3','product_category_4','product_category_5','product_category_6','product_category_7',
                          'product_country','product_id','product_title','partner_id','user_id']


    def split_df(self):
        df_raw=pd.read_csv(self.path,sep="\t",nrows=self.nrows,header=None,names=self.header_info,low_memory=False)
        list_of_small_files=[]
        df_raw["click_timestamp"] = [datetime.datetime.utcfromtimestamp(x).date() for x in df_raw["click_timestamp"]]

        df_raw.sort_values(["click_timestamp"], ascending=True, inplace=True)
        self.dtypes=df_raw.dtypes
        with open('dtypes', 'wb') as handle:
            pickle.dump(self.dtypes, handle, protocol=pickle.HIGHEST_PROTOCOL)
        list_of_dfs = {}
        for id, group in df_raw.groupby("partner_id"):
            p = os.path.join(os.getcwd(), "splitted data\data_{}.csv".format(id.lower()))
            group.to_csv(p, index=False)
            if group.shape[0]<67000:
                list_of_small_files.append(id)
            temp_df=pd.DataFrame(group)
            list_of_dfs[id]={}
            for day, group_day in temp_df.groupby("click_timestamp"):
                temp_dict=pd.DataFrame(group_day)
                list_of_dfs[id][day]={"df_data":temp_dict}
        self.list_of_dfs = list_of_dfs
        with open('list of small files', 'wb') as handle:
            pickle.dump(list_of_small_files, handle, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    path="E:\Criteo_Conversion_Search\CriteoSearchData"
    splitter = partners_data_splitter(path, None, None)
    splitter.split_df()

    print("start")

