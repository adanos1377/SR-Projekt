import json
import os
import sys

import optimizer


class per_partner_simulator:
    def __init__(self,id,click_cost,how_many,seed,cost,npm):
        self.partner_id=id
        self.optimizer=optimizer.optimizer(seed,how_many,id)
        self.npm=npm
        self.cost=cost
        self.date=None
        self.excluded_products=[]
        self.first_day=True
        self.click_cost=click_cost

    def next_day(self, today_data,date):
        today_data_without_excluded_products=today_data
        if self.excluded_products!=[]:
            today_data_without_excluded_products=today_data_without_excluded_products[today_data_without_excluded_products['product_id'].apply(lambda x:x not in self.excluded_products)]
        self.date=date
        log={}

        if today_data.shape[0]>1:
            orig_stdout = sys.stdout
            sys.stdout = open("exclusion_log.txt", "a")
            print('Date: ', self.date)
            print('number of to be excluded products: ',len(self.excluded_products))
            print('list of products to be excluded: ',self.excluded_products)
            sys.stdout.close()
            sys.stdout = orig_stdout
        log["day"]=self.date


        results,actuallyexcluded=self.calculate_per_day_profit_gain_factors(today_data)

        excluded_products,seenSoFar=self.optimizer.next_day(today_data_without_excluded_products, self.date)
        log["productsSeenSoFar"] = seenSoFar
        log["productsToExclude"] = sorted(self.excluded_products)
        log["productsActuallyExcluded"] = sorted(actuallyexcluded)
        self.excluded_products=excluded_products
        return results,log
    def calculate_per_day_profit_gain_factors(self,today_data):
        actually_excluded = []
        if self.first_day:
            self.first_day=False
            click_savings=0.0
            sale_losses=0.0
            profit_losses=0.0
            profit_gain=0.0
        else:
            all_products=today_data['product_id'].unique()
            click_savings_for_each_product=[]
            sale_losses_for_each_product = []
            profit_losses_for_each_product = []

            if self.excluded_products!=[]:
                for product in self.excluded_products:
                    if product in all_products:
                        actually_excluded.append(product)
                        product_data=today_data[today_data["product_id"]==product]
                        clicks_saved=today_data['product_id'].value_counts()[product]
                        click_savings_for_each_product.append(clicks_saved * self.click_cost)
                        sales_lost=0.0
                        for x,row in product_data.iterrows():
                            if row['Sale']==1:
                                sales_lost+=row['SalesAmountInEuro']
                        sale_losses_for_each_product.append(sales_lost)
                        profit_losses_for_each_product.append(sales_lost*(self.npm+self.cost))
            orig_stdout = sys.stdout
            sys.stdout = open("exclusion_log.txt", "a")
            print('number of actually excluded products: ',len(actually_excluded))
            print('list of actually excluded products: ',actually_excluded)
            sys.stdout.close()
            sys.stdout = orig_stdout

            click_savings=0.0
            sale_losses=0.0
            profit_losses=0.0
            for c in click_savings_for_each_product:
                click_savings+=c
            for s in sale_losses_for_each_product:
                sale_losses+=s
            for p in profit_losses_for_each_product:
                profit_losses+=p
            profit_gain = click_savings - (profit_losses)
        result={}
        result['click_savings']=click_savings
        result['sale_losses']=sale_losses
        result['profit_losses']=profit_losses
        result['profit_gain']=profit_gain
        print('results for: ',self.partner_id, ',', self.date, ':', result)
        return result,actually_excluded