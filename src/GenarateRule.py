class GenarateRule:

    selection_counter = 0


#-------------------------Constructor------------------------#

    def __init__(self, mapped_project, mapped_data_source, mapped_fields):
        self.mapped_project = mapped_project
        self.mapped_data_source = mapped_data_source
        self.mapped_fields = mapped_fields
        self.rule = {   "logsource:": {"product:": [], "service:": []},
                        "detection:": { "condition:": {}},
                        "field:": []}



#--------------------------Functions-------------------------#


#TODO: assign self.mapped_project into self.rule
    def assign_project(self):
        self.rule["field:"] = self.mapped_project
        

    def assign_logsource(self):
        #TODO: assign self.mapped_logsource into self.final_dict
        products, services = self.mapped_data_source
        self.rule["logsource:"]["product:"] = products
        self.rule["logsource:"]["service:"] = services
        

    def assign_fields(self):
        #TODO: assign self.mapped_fields into self.final_dict

        



        return

    def finalize_rule(self):
        #TODO: convert self.final_dict to string according by sigma rule
        return  # final string to print
