import re
from mapping.products import kql_product_mapping
from mapping.services import kql_service_mapping

kql = """
    events_all
    | where data_source_type_id=12 or data_source_type_id =    13 or data_source_type_id in (  21, 31 , 54 , 86  ) or data_source_type_id in   (21,   87,64)"""

#TODO:check if the given expression is a legal KQL query



#-------------------- Handle logsource --------------------#

pattern = r"data_source_type_id\s*=\s*(\d+)|data_source_type_id\s+in\s*\(\s*(\d+(?:\s*,\s*\d+)*)\s*\)"


#Step 1: get the numbers.
matches = re.findall(pattern, kql)

numbers = []

for match in matches:
    if match[0]:  # If the first group (for = ) is not empty
        numbers.append(int(match[0]))
    if match[1]:  # If the second group (for in () ) is not empty
        numbers.extend(map(int, match[1].split(',')))

print(numbers)
    

#Step 2: get the relevent products and services

products = []
services = []


for num in numbers:
    product_matches = [value for key, value in kql_product_mapping.items() 
                        if (isinstance(key, tuple) and num in key) or (key == num)]
    
    service_matches = [value for key, value in kql_service_mapping.items() 
                        if (isinstance(key, tuple) and num in key) or (key == num)]
    
    if not product_matches and not service_matches:
        print(f"ERROR: the number : {num} did not match any key in either mapping")
        break
    
    products.extend(product_matches)
    services.extend(service_matches)


services = [item for sublist in services for item in (sublist if isinstance(sublist, list) else [sublist])]
            
print(f"Products: {products}\n")
print(f"Services: {services}\n")















    





#handle logsource
    
    #handle product

    #handle service




























#check if kql is a legal KQL expression

#data_source_type_id 































kql2 = """
    events_all
    | where data_source_type_id in (456, 460, 501, 502, 507, 440, 347) and _eventSource =~ 'config.amazonaws.com' and (_eventName in~ ('DeleteDeliveryChannel', 'StopConfigurationRecorder'))"""



rule2 = """
logsource:
    product: aws
    service: cloudtrail
detection:
    selection_source:
        eventSource: config.amazonaws.com
        eventName:
            - DeleteDeliveryChannel
            - StopConfigurationRecorder
    condition: selection_source

    falsepositives:
    - Valid change in AWS Config Service
level: high

            - DeleteDeliveryChannel
            - StopConfigurationRecorder
    condition: selection_source
falsepositives:
            - DeleteDeliveryChannel
            - StopConfigurationRecorder
    condition: selection_source
            - DeleteDeliveryChannel
            - StopConfigurationRecorder
            - DeleteDeliveryChannel
            - DeleteDeliveryChannel
            - StopConfigurationRecorder
    condition: selection_source
falsepositives:
    - Valid change in AWS Config Service
level: high
"""







