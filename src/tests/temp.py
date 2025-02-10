

#------------------------TESTING (TEMPORARY)----------------------#
# query = ("events_all\n| where data_source_type_id==11 and _CommandLine contains 'base64' and ((_CommandLine contains '|bash' or _CommandLine contains '|sh' or _CommandLine contains '|bash' or _CommandLine contains '|sh') or (_CommandLine endswith '|sh' or _CommandLine endswith '|bash' or _CommandLine endswith '|sh' or _CommandLine endswith '|bash'))")
# query = ("events_all\n| project _Hashes \n | where data_source_type_id in (456, 460, 501, 502, 507, 440, 347) and _eventSource =~ 'lambda.amazonaws.com' and  _eventName startswith 'UpdateFunctionConfiguration' and _destination.port in (8080, 21, 80, 23, 50000, 1521, 27017, 1433, 11211, 3306, 15672, 5900, 5901, 5902, 5903, 5904) ")
# query= "events_all\n| where data_source_type_id in (456, 460, 501, 502, 507, 440, 347) and (_eventSource =~ 'sts.amazonaws.com' and _eventName =~ 'AssumeRoleWithSAML') or (_eventSource =~ 'iam.amazonaws.com' and _eventName =~ 'UpdateSAMLProvider')"
# #
# parse_query = Query(query)
# print(parse_query.map_project())
# print(parse_query.map_data_source())
# print(parse_query.map_field(parse_query.fields.copy()))



# events_all
# | where data_source_type_id in (456, 460, 501, 502, 507, 440, 347) and _eventSource =~ 'lambda.amazonaws.com' or _eventName startswith 'UpdateFunctionConfiguration'
#
# logsource:
#     product: aws
#     service: ..
# detection:
#     selection:
#         eventSource: lambda.amazonaws.com
#         eventName|startswith: 'UpdateFunctionConfiguration'
#     condition: selection




#------------------------EXAMPLE----------------------#

# query= "events_all\n| where data_source_type_id in (456, 460, 501, 502, 507, 440, 347) and (_eventSource =~ 'sts.amazonaws.com' and _eventName =~ 'AssumeRoleWithSAML') or (_eventSource =~ 'iam.amazonaws.com' and _eventName =~ 'UpdateSAMLProvider')"
# parse_query = Query(query)
# print(f' data source: {parse_query.map_data_source()}')
# print(f' fields: {parse_query.map_field(parse_query.fields.copy())}')
#
# '''fields: {'logical operation': 'or', 'operands': [{'logical operation': 'and',
#                                                   'operands': [('eventSource', '=~', "'sts.amazonaws.com'"),
#                                                                ('eventName', '=~', "'AssumeRoleWithSAML'")]},
#                                                  {'logical operation': 'and',
#                                                   'operands': [('eventSource', '=~', "'iam.amazonaws.com'"),
#                                                                ('eventName', '=~', "'UpdateSAMLProvider'")]}]}'''
