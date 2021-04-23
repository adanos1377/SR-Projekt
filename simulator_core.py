import datetime
import partners_data_reader
import per_partner_simulator

class simulator_core:
    def __init__(self, partners_to_involve_in_simulation,partners_to_read_data_from,seed,how_many_ratio,npm,cost,partners_cost_dict):
        self.partners_to_involve_in_simulation=partners_to_involve_in_simulation
        self.partners_to_read_data_from=partners_to_read_data_from
        self.partners_data_reader=partners_data_reader.partners_data_reader(partners_to_read_data_from)
        self.today_partners_data_dict = None
        self.partners_simulators=[]
        self.all_partners_results_dict = {}
        for id in partners_to_involve_in_simulation:
            self.partners_simulators.append(per_partner_simulator.per_partner_simulator(id,partners_cost_dict[id],how_many_ratio,seed,cost,npm))
            self.all_partners_results_dict[id] = {}

    def next_day(self):
        self.today_partners_data_dict,dates=self.partners_data_reader.next_day()
        for partner in self.partners_simulators:
            single_partner_result_dict,log=partner.next_day(self.split_many_partners_data(partner.partner_id),datetime.datetime.strftime(dates[partner.partner_id], '%Y-%m-%d'))
            self.all_partners_results_dict[partner.partner_id] = (single_partner_result_dict)
        return self.all_partners_results_dict,log
    def split_many_partners_data(self,id):
        return self.today_partners_data_dict[id]


