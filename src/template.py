import re
from mapping.products import kql_product_mapping
from mapping.services import kql_service_mapping



query = "events_all| project _Hashes | where data_source_type_id in (456, 460, 501, 502, 507, 440, 347) and _eventSource =~ 'lambda.amazonaws.com' and _eventName startswith 'UpdateFunctionConfiguration'  | project 'hi' , 'n' "

def extract_fields(query):
    start_index = query.find("where") + len("where")

    if start_index == -1 : 
        return ""
    else :
        query_after_where = query[start_index:]

    res = re.sub(r"(?:and|or)?\s*data_source_type_id\s*(?:=\s*\d+|in\s*\(\s*\d+(?:\s*,\s*\d+)*\s*\))\s*(?:and|or)?",
                     "", query_after_where)
    res = re.sub(r"\|\s*project\s+([^\|]+)", "" , res)
    
    return res.strip(" ")


print(extract_fields(query))




    # def extract_project(self, query):
    #     regex = r"(?<=\|)\s*project\s+([^\|]+)"
    #     matches = re.findall(regex, query)
    #     if not matches:
    #         raise ValueError("Illegal input: Expected a project.")
    #     project = []
    #     for match in matches:
    #         col_to_check = [col.strip() for col in match.split(',')]
    #         print (col_to_check)
    #         if "" in col_to_check:
    #             raise ValueError("Illegal input: Expected a project.")
    #         project.extend(col_to_check)
    #
    #     return project
















































#-------------------- Handle logsource --------------------#

#pattern = r"data_source_type_id\s*=\s*(\d+)|data_source_type_id\s+in\s*\(\s*(\d+(?:\s*,\s*\d+)*)\s*\)"




'''#Step 1: get the id-s numbers.
matches = re.findall(pattern, kql)

numbers = []

for match in matches:
    if match[0]:  # If the first group (for = ) is not empty
        numbers.append(int(match[0]))
    if match[1]:  # If the second group (for in () ) is not empty
        numbers.extend(map(int, match[1].split(',')))

print(numbers)
    

#Step 2: get the matches products and services.
products = set()
services = set()

for num in numbers:

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
  
            
print(f"Products: {products}\n")
print(f"Services: {services}\n")
'''