
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


file_and_dir_field_mapping = {
    "CallerProcessName": DIR_PATH_FILE_NAME,
    "FileName": DIR_PATH_FILE_NAME,
    "Filename": DIR_PATH_FILE_NAME,
    "HostApplication": DIR_PATH_FILE_NAME,
    "Image": DIR_PATH_FILE_NAME,
    "ImageLoaded": DIR_PATH_FILE_NAME,
    "ImageName": DIR_PATH_FILE_NAME,
    "ImagePath": DIR_PATH_FILE_NAME,
    "Name": DIR_PATH_FILE_NAME,
    "OriginalFileName": DIR_PATH_FILE_NAME,
    "ParentImage": DIR_PATH_FILE_PARENT_NAME,
    "Path": DIR_PATH_FILE_PARENT_NAME,
    "ProcessName": DIR_PATH_FILE_NAME,
    "ProcessPath": DIR_PATH_FILE_NAME,
    "RelativeTargetName": DIR_PATH_FILE_NAME,
    "Service": DIR_PATH_FILE_NAME,
    "ServiceFileName": DIR_PATH_FILE_NAME,
    "SourceFilename": DIR_PATH_FILE_NAME,
    "SourceImage": DIR_PATH_FILE_NAME,
    "StartModule": DIR_PATH_FILE_NAME,
    "TargetFilename": DIR_PATH_FILE_NAME,
    "TargetImage": DIR_PATH_FILE_NAME,
    "name": DIR_PATH_FILE_NAME,
    "path": DIR_PATH_FILE_NAME,
    "process": DIR_PATH_FILE_NAME,
    "processPath": DIR_PATH_FILE_NAME,
}

ip_field_mapping = {
    "Address": {
        IPV4: ["_ipv4", "_dst_ipv4", "_src_ipv4"],
        IPV6: ["_ipv6", "_dst_ipv6", "_src_ipv6"]
    },
    "DestinationIp": {
        IPV4: ["_dst_ipv4"],
        IPV6: ["_dst_ipv6"]
    },
    "IpAddress": {
        IPV4: ["_ipv4", "_dst_ipv4", "_src_ipv4"],
        IPV6: ["_ipv6", "_dst_ipv6", "_src_ipv6"],
    },
    "IPaddress": {
        IPV4: ["_ipv4", "_dst_ipv4", "_src_ipv4"],
        IPV6: ["_ipv6", "_dst_ipv6", "_src_ipv6"],
    },
    "dst_ip": {
        IPV4: ["_dst_ipv4"],
        IPV6: ["_dst_ipv6"]
    },
    "src_ip": {
        IPV4: ["_src_ipv4"],
        IPV6: ["_src_ipv6"]
    }
}

 #ip_field_values = set(val for values in ip_field_mapping.values() for value in
 #                      values.values() for val in value)

string_value_field_mapping = {
    "EventID": "_EventID",
    "LogonType": "_LogonType",
}

list_str_value_field_mapping = [
        "_Message",
        "_Protocol"
]

list_int_value_field_mapping = [
    "matchedTypes"
]

list_value_field_mapping = list_str_value_field_mapping + list_int_value_field_mapping

kql_field_mapping = {
    **field_mapping, **string_value_field_mapping, **file_and_dir_field_mapping
     ,**ip_field_mapping
}