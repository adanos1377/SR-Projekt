#czyta dane wszystkich partnerów wyznaczonych do symulacji
import os
import pandas as pd
import datetime

class partners_data_reader:
    def __init__(self, partners_to_read_data_from):
        self.list_of_ids=partners_to_read_data_from
        self.source_of_dfs={}
        self.first_day=True
        self.dates={}
        for id in self.list_of_ids:
            p = os.path.join(os.getcwd(), "splitted data\data_{}.csv".format(id.lower()))
            df = pd.read_csv(p, low_memory=False)
            self.source_of_dfs[id]=df
            self.dates[id]=self.get_earliest_date(df)

    def get_earliest_date(self,df):
        return datetime.datetime.strptime(df["click_timestamp"].iloc[0],'%Y-%m-%d').date()
    def next_day(self):
        data_for_next_day={}
        for id in self.list_of_ids:
            data_for_next_day[id] = self.__get_next_day_partner_data(id)
        return data_for_next_day,self.dates
    def __get_next_day_partner_data(self,id):
        if self.first_day==True:
            df = self.source_of_dfs[id][self.source_of_dfs[id]["click_timestamp"] == datetime.datetime.strftime(self.dates[id], '%Y-%m-%d')]
            self.first_day=False
        else:
            self.dates[id]=self.dates[id] + datetime.timedelta(days=1)
            df=self.source_of_dfs[id][self.source_of_dfs[id]["click_timestamp"]==datetime.datetime.strftime(self.dates[id],'%Y-%m-%d')]
        return df


