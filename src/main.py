import yaml
from KQL import KQL
from SigmaRuleGenerator import SigmaRuleGenerator


def main():
    query_input = input("Enter a query: ")
    parsed_query = KQL.parse(query_input)
    rule_generator = SigmaRuleGenerator()
    rule = rule_generator.from_query(parsed_query)
    print(rule)
    print(yaml.dump(rule, default_flow_style=False))

if __name__ == "__main__":
    main()

#-------------------examples of queries------------------------#
 # query1 = events_all\n| where data_source_type_id==11 and _CommandLine contains 'base64' and ((_CommandLine contains '| bash' or _CommandLine contains '| sh' or _CommandLine contains '|bash' or _CommandLine contains '|sh') or (_CommandLine endswith '|sh' or _CommandLine endswith '|bash' or _CommandLine endswith '|sh' or _CommandLine endswith '|bash'))
 # query2 = events_all\n| where _CommandLine contains 'base64' and _CommandLine contains '|bash' 
 # query3 = events_all\n| where data_source_type_id in (456, 460, 501, 502, 507, 440, 347) and _eventSource =~ 'lambda.amazonaws.com' and  _eventName startswith 'UpdateFunctionConfiguration' and _destination.port in (8080, 21, 80, 23, 50000, 1521, 27017, 1433, 11211, 3306, 15672, 5900, 5901, 5902, 5903, 5904) 
 # query4 = events_all\n| where data_source_type_id in (456, 460, 501, 502, 507, 440, 347) and (_eventSource =~ 'sts.amazonaws.com' and _eventName =~ 'AssumeRoleWithSAML') or (_eventSource =~ 'iam.amazonaws.com' and _eventName =~ 'UpdateSAMLProvider')
 # query5 = events_all| where data_source_type_id in (456, 460, 501, 502, 507, 440, 347) and _eventSource =~ 'lambda.amazonaws.com' or _eventName startswith 'UpdateFunctionConfiguration'


