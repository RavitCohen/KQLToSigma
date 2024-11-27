class GenarateRule:

    def __init__(self, mapped_project, mapped_logsource, mapped_fields):
        self.mapped_project = mapped_project
        self.mapped_logsource = mapped_logsource
        self.mapped_fields = mapped_fields
        self.final_dict = {"logsource:": {"product:": {}, "service:": {}},
                           "detection:": {"selection:": {}, "condition:": {}},
                           "field:": {}}

    def assign_project(self):
        #TODO: assign self.mapped_project into self.final_dict
        return

    def assign_logsource(self):
        #TODO: assign self.mapped_logsource into self.final_dict
        return

    def assign_fields(self):
        #TODO: assign self.mapped_fields into self.final_dict
        return

    def finalize_rule(self):
        #TODO: convert self.final_dict to string according by sigma rule
        return  # final string to print
