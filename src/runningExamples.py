import json
import os
from Query import Query
import yaml


current_dir = os.path.dirname(os.path.abspath(__file__))
json_file_path = os.path.join(current_dir, "../examples/sigma_to_kql_starship_fields.json")
json_file_path = os.path.normpath(json_file_path)

with open(json_file_path ,'r' ) as file:
    json_data = json.load(file)
    

for item in json_data:
    
    kql= item["pysigma_kql"]
    #result = Query(kql).parse_to_rule()
    correct_rule = item["sigma_rule"]
    
    #STEP 1: project KQL
    print("given kql query:\n")
    print(kql)
    print("\n")
    
    #STEP 2: project correct Sigma Rule
    print("correct sigma rule:\n")
    print(yaml.dump(correct_rule, default_flow_style=False))
    
    #STEP 3: project our result
    # print("our sigma_rule:\n")
    # print(yaml.dump(result, default_flow_style=False))
    print("\n---------------------------------------------\n")