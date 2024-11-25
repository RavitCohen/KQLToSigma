import re
from mapping.products import kql_product_mapping
from mapping.services import kql_service_mapping

kql = """
    events_all
    | where data_source_type_id=12 or data_source_type_id =    13 or data_source_type_id in (  11, 31 , 54 , 446  ) or data_source_type_id in   (21,   87,64)"""

#TODO:check if the given expression is a legal KQL query



#-------------------- Handle logsource --------------------#

pattern = r"data_source_type_id\s*=\s*(\d+)|data_source_type_id\s+in\s*\(\s*(\d+(?:\s*,\s*\d+)*)\s*\)"


#Step 1: get the id-s numbers.
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

