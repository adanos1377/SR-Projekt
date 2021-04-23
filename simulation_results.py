class simulation_results:
    def __init__(self,partners):
        self.partners=partners
        self.list_of_individual_partners_results={}
        for partner in partners:
            self.list_of_individual_partners_results[partner]=[]
    def results_for_each_partner(self):
        return self.list_of_individual_partners_results
    def aggregated_results_for_all_partners(self):
        all_partners={}
        all_partners['click_savings'] = 0
        all_partners['sale_losses'] = 0
        all_partners['profit_losses'] = 0
        all_partners['profit_gain'] = 0
        for partner in self.partner_aggregated:
            all_partners['click_savings'] += self.partner_aggregated[partner]['click_savings']
            all_partners['sale_losses'] = self.partner_aggregated[partner]['sale_losses']
            all_partners['profit_losses'] = self.partner_aggregated[partner]['profit_losses']
            all_partners['profit_gain'] = self.partner_aggregated[partner]['profit_gain']
        return all_partners
    def aggregated_results_for_each_partner(self):
        partner_aggregated={} # słownik partner:zagregowane wyniki
        for partner in self.list_of_individual_partners_results:
            list_of_dict=self.list_of_individual_partners_results[partner]
            partner_aggregated[partner]={}
            partner_aggregated[partner]['click_savings'] =0
            partner_aggregated[partner]['sale_losses'] = 0
            partner_aggregated[partner]['profit_losses'] = 0
            partner_aggregated[partner]['profit_gain'] = 0
            for result in list_of_dict: # result to słownik z listy
                partner_aggregated[partner]['click_savings']+=result['click_savings']
                partner_aggregated[partner]['sale_losses']+=result['sale_losses']
                partner_aggregated[partner]['profit_losses']+=result['profit_losses']
                partner_aggregated[partner]['profit_gain']+=result['profit_gain']
        self.partner_aggregated=partner_aggregated
        return partner_aggregated
    def add_daily_results(self,daily_results):
        for id in daily_results:
            self.list_of_individual_partners_results[id].append(daily_results[id])