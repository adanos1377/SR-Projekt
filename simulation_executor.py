import partners_data_reader
import partners_profiles
import simulation_results
import simulator_core
import json
import matplotlib.pyplot as plt
class simulation_executor:
    def __init__(self):
        with open('sim_conf') as json_file:
            config = json.load(json_file)
        self.days = config["number_of_simulation_steps"]
        self.cost=config["cost"]
        self.partners_for_simulation=config["partners_to_involve_in_simulation"]
        self.partners_to_read_data_from=config["partners_to_read_data_from"]
        self.npm=config["npm"]
        self.seed=config["seed"]
        self.how_many_ratio=config["how_many_ratio"]
    def graph_profit_gain(self,partner):
        temp=[]
        res=self.resulter.results_for_each_partner()[partner]
        for day in range(0, self.days):
            temp.append(res[day]['profit_gain'])

        plt.plot(range(1, self.days + 1), temp)
        plt.xlabel('days')
        plt.ylabel('EURO')
        plt.title('profit_gain')
        plt.show()
    def graph_accumulated_profit_gain(self,partner):
        temp = [0]
        res = self.resulter.results_for_each_partner()[partner]
        for day in range(0, self.days):
            temp.append(res[day]['profit_gain']+temp[-1])
        temp.pop()
        plt.plot(range(1, self.days + 1), temp)
        plt.xlabel('days')
        plt.ylabel('EURO')
        plt.title('accumulated_profit_gain')
        plt.show()
    def graph_clicks_savings(self,partner):
        temp=[]
        res=self.resulter.results_for_each_partner()[partner]
        for day in range(0, self.days):
            temp.append(res[day]['click_savings'])

        plt.plot(range(1, self.days + 1), temp)
        plt.xlabel('days')
        plt.ylabel('EURO')
        plt.title('clicks_savings')
        plt.show()
    def graph_sale_losses(self,partner):
        temp=[]
        res=self.resulter.results_for_each_partner()[partner]
        for day in range(0, self.days):
            temp.append(res[day]['sale_losses'])

        plt.plot(range(1, self.days + 1), temp)
        plt.xlabel('days')
        plt.ylabel('EURO')
        plt.title('sale_losses')
        plt.show()
    def graph_profit_losses(self,partner):
        temp=[]
        res=self.resulter.results_for_each_partner()[partner]
        for day in range(0, self.days):
            temp.append(res[day]['profit_losses'])

        plt.plot(range(1, self.days + 1), temp)
        plt.xlabel('days')
        plt.ylabel('EURO')
        plt.title('profit_losses')
        plt.show()
    def execute_simulation(self):
        log_days = []
        self.profiles=partners_profiles.partners_profiles(self.partners_for_simulation,self.cost)
        self.partners_cost_dict=self.profiles.read_partners_profiles()
        self.pdr = partners_data_reader.partners_data_reader(self.partners_to_read_data_from)
        self.resulter = simulation_results.simulation_results(self.partners_for_simulation)
        self.simulation_core=simulator_core.simulator_core(self.partners_for_simulation,self.partners_to_read_data_from,self.seed,self.how_many_ratio,self.npm,self.cost,self.partners_cost_dict)
        for x in range(self.days):
            daily_result,log=self.simulation_core.next_day()
            self.resulter.add_daily_results(daily_result)
            log_days.append(log)
        results = {
            'for_individual_partners': self.resulter.results_for_each_partner(), # Słownik= {klucz=id:wartość=lista słowników results each day}
            'aggregated_for_each_partner': self.resulter.aggregated_results_for_each_partner(),
            'summed_for_all_partners': self.resulter.aggregated_results_for_all_partners(),
        }
        with open('simulation_results.json', 'w') as fp:
            json.dump(results, fp, separators=(',', ':'))

        logi = {
            'strategy': "random",
            'days': log_days  # lista Słowników
        }
        with open("log_for_" + self.partners_for_simulation[0] + ".json", 'w') as fp:
            json.dump(logi, fp, separators=(',', ':'))


        for id in self.partners_for_simulation:
            self.graph_clicks_savings(id)
            self.graph_sale_losses(id)
            self.graph_profit_losses(id)
            self.graph_profit_gain(id)
            self.graph_accumulated_profit_gain(id)

if __name__ == '__main__':
    simulation=simulation_executor()
    simulation_executor().execute_simulation()

