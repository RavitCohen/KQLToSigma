import re;
from mapping.products import kql_product_mapping
from mapping.services import kql_service_mapping

class Query:
    def __init__(self, KQL_to_map):
        #Step 1: parse table
        # TODO: self.table =

        # Step 2: parse project
        # TODO: self.project =

        # Step 3: parse logsource
        pattern = r"data_source_type_id\s*=\s*(\d+)|data_source_type_id\s+in\s*\(\s*(\d+(?:\s*,\s*\d+)*)\s*\)"
        matches = re.findall(pattern, KQL_to_map)
        numbers = []
        for match in matches:
            if match[0]:  # If the first group (for = ) is not empty
                numbers.append(int(match[0]))
            if match[1]:  # If the second group (for in () ) is not empty
                numbers.extend(map(int, match[1].split(',')))
        self.logsource=numbers

        # Step 4: parse fields
        # TODO: self.fields =

    def handle_project(self):
        return

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

    def handle_fields(self):
        return