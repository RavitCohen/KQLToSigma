
DIR_PATH_FILE_NAME = "_fileName"
DIR_PATH_FILE_PARENT_NAME = "_fileParentName"
IPV4 = "ipv4"
IPV6 = "ipv6"

field_mapping = {
    "_AccountName": "AccountName",
    "_AttributeLDAPDisplayName": "AttributeLDAPDisplayName",
    "_Category": "Category",
    "_ClientProcessId": "ClientProcessId",
    "_CommandLine": "CommandLine",
    "_Company": "Company",
    "_Description": "Description",
    "_DestPort": "DestPort",
    "_DestinationPort": "DestinationPort",
    "_DestinationHostname": "DestinationHostname",
    "_DeviceDetail.deviceId": "DeviceDetail.deviceId",
    "_eventName": "eventName",
    "_Hashes": "Hashes",
    "_HostName": "HostName",
    "_Initiatedby": "Initiatedby",
    "_LogonProcessName": "LogonProcessName",
    "_Message": "Message",
    "_NewTargetUserName": "NewTargetUserName",
    "_ObjectName": "ObjectName",
    "_ParentCommandLine": "ParentCommandLine",
    "_ParentProcessId": "ParentProcessId",
    "_Payload": "Payload",
    "_ProcessId": "ProcessId",
    "_Product": "Product",
    "_properties.message": "properties.message",
    "_Protocol": "Protocol",
    "_Provider_Name": "Provider_Name",
    "_QNAME": "QNAME",
    "_QueryName": "QueryName",
    "_SamAccountName": "SamAccountName",
    "_ScriptBlockText": "ScriptBlockText",
    "_ServiceName": "ServiceName",
    "_SourcePort": "SourcePort",
    "_SubjectUserName": "SubjectUserName",
    "_SubjectUserSid": "SubjectUserSid",
    "_TargetObject": "TargetObject",
    "_TargetUserName": "TargetUserName",
    "_TargetUserSid": "TargetUserSid",
    "_USER": "USER",
    "_User": "User",
    "_UserName": "UserName",
    "_Username": "Username",
    "_cs-username": "cs-username",
    "_destination.port": "destination.port",
    "_dst_port": "dst_port",
    "_eventSource": "eventSource",
    "_EventType": "EventType",
    "_md5": "md5",
    "_payload": "payload",
    "_sha1": "sha1",
    "_sha256": "sha256",
    "_userAgent": "userAgent",
    "_user_agent": "user_agent",
}

# Todo: handle with this specipic case
file_and_dir_field_mapping = {
    DIR_PATH_FILE_NAME: ["CallerProcessName","FileName","Filename", "HostApplication" , "Image", "ImageLoaded","ImageName","ImagePath", "Name", "OriginalFileName"],
    DIR_PATH_FILE_PARENT_NAME: ["ParentImage", "Path", "ProcessName","ProcessPath", "RelativeTargetName", "Service", "ServiceFileName", "SourceFilename", "SourceImage", "StartModule", "TargetFilename", "TargetImage", "name", "path", "process", "processPath"]
}

# Todo: or between them
ip_field_mapping = {
    "_ipv4": [ "Address", "IpAddress", "IPaddress"],
    "_dst_ipv4": [ "Address", "DestinationIp", "IpAddress", "IPaddress", "dst_ip"],
    "_src_ipv4": [ "Address", "IpAddress", "IPaddress", "src_ip"],
    "_ipv6": ["Address", "IpAddress", "IPaddress"],
    "_dst_ipv6": ["Address", "DestinationIp", "IpAddress", "IPaddress", "dst_ip"],
    "_src_ipv6": ["Address", "IpAddress", "IPaddress", "src_ip"],

}

 # ip_field_values = set(val for values in ip_field_mapping.values() for value in
 #                      values.values() for val in value)

string_value_field_mapping = {
    "_EventID": "EventID",
    "_LogonType": "LogonType",
}

# list_str_value_field_mapping = [
#         "_Message",
#         "_Protocol"
# ]
#
# list_int_value_field_mapping = [
#     "matchedTypes"
# ]
#
# list_value_field_mapping = list_str_value_field_mapping + list_int_value_field_mapping

kql_field_mapping = {
    **field_mapping, **string_value_field_mapping, **file_and_dir_field_mapping
     ,**ip_field_mapping
}