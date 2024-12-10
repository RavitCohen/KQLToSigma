import re;
from mapping.products import kql_product_mapping
from mapping.services import kql_service_mapping
from GenarateRule import *

class Query:

#-------------------------Constructor------------------------#

    def __init__(self, query):
        
        self.table = self.extractTable(query)
        self.project = self.extractProject(query)
        self.logsoure = self.extractLogsource(query)
        self.fields = self.extractFields(query)


#----------------Constructor's Helper Functions---------------#

    def extractTable(self, query):
        regex = r"^(\S+)\s*\r?\n?\|"
        match = re.match(regex, query)

        if match:
            return match.group(1)
        else:
            raise ValueError("Illegal input: Expected a table.")
    

    def extractProject(self,query):
        regex = r"(?<=\|)\s*project\s+([^\|]+)"
        matches = re.findall(regex, query)

        project = []
        for match in matches:
            project.extend([col.strip() for col in match.split(',')])

        return project


    def extractLogsource(self, query):
        pattern = r"data_source_type_id\s*=\s*(\d+)|data_source_type_id\s+in\s*\(\s*(\d+(?:\s*,\s*\d+)*)\s*\)"
        matches = re.findall(pattern, query)
        numbers = []
        
        for match in matches:
            if match[0]:  # If the first group (for = ) is not empty
                numbers.append(int(match[0]))
            if match[1]:  # If the second group (for in () ) is not empty
                numbers.extend(map(int, match[1].split(',')))
        self.logsource=numbers

        return numbers

#TODO: decide what to do with this according to the implementation
    def extractFields(self, query):
        
        new_query = re.sub(r"^[^\|]*\|", "", query, count=1)
        new_query = re.sub(r"\|?\s*project[^\n]*\n?", "", new_query)
        new_query = re.sub(r"data_source_type_id\s*(=|in)\s*\([^\)]+\|\s*\d+\)\s*and?\s*", "", new_query)
    

#--------------------------Functions-------------------------#


    def handle_logsource(self):
        products = set()
        services = set()

        for num in self.logsource:

            collected_products = {kql_product_mapping[num]} if num in kql_product_mapping else set()

            if num in kql_service_mapping:
                value = kql_service_mapping[num]
                collected_services = set(value) if isinstance(value, list) else {value}
            else:
                collected_services = set()

            if not collected_products and not collected_services:
                print(f"ERROR: the number {num} did not match any key in either mapping!")
                break

            products = products.union(collected_products)
            services = services.union(collected_services)

        return products, services

    
    #TODO: implement after we'll get a fields mapping
    def handle_project(self):
        pass


    def parse_to_rule(self):
        
        mapped_project = self.handle_project()
        mapped_logsource = self.handle_logsource()
        mapped_fields = self.handle_fields()
        
        rule = GenarateRule(mapped_project, mapped_logsource, mapped_fields)
        
        return rule.finalize_rule()



