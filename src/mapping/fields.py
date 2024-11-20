#from ..pySigma_QRadar_base.QRadarPipeline import IPV4, IPV6

DIR_PATH_FILE_NAME = "_fileName"
DIR_PATH_FILE_PARENT_NAME = "_fileParentName"

field_mapping = {
    "AccountName": "_AccountName",
    "AttributeLDAPDisplayName": "_AttributeLDAPDisplayName",
    "Category": "_Category",
    "ClientProcessId": "_ClientProcessId",
    "CommandLine": "_CommandLine",
    "Company": "_Company",
    "Description": "_Description",
    "DestPort": "_DestPort",
    "DestinationPort": "_DestinationPort",
    "DestinationHostname": "_DestinationHostname",
    "DeviceDetail.deviceId": "_DeviceDetail.deviceId",
    "eventName": "_eventName",
    "Hashes": "_Hashes",
    "HostName": "_HostName",
    "Initiatedby": "_Initiatedby",
    "LogonProcessName": "_LogonProcessName",
    "Message": "_Message",
    "NewTargetUserName": "_NewTargetUserName",
    "ObjectName": "_ObjectName",
    "ParentCommandLine": "_ParentCommandLine",
    "ParentProcessId": "_ParentProcessId",
    "Payload": "_Payload",
    "ProcessId": "_ProcessId",
    "Product": "_Product",
    "properties.message": "_properties.message",
    "Protocol": "_Protocol",
    "Provider_Name": "_Provider_Name",
    "QNAME": "_QNAME",
    "QueryName": "_QueryName",
    "SamAccountName": "_SamAccountName",
    "ScriptBlockText": "_ScriptBlockText",
    "ServiceName": "_ServiceName",
    "SourcePort": "_SourcePort",
    "SubjectUserName": "_SubjectUserName",
    "SubjectUserSid": "_SubjectUserSid",
    "TargetObject": "_TargetObject",
    "TargetUserName": "_TargetUserName",
    "TargetUserSid": "_TargetUserSid",
    "USER": "_USER",
    "User": "_User",
    "UserName": "_UserName",
    "Username": "_Username",
    "cs-username": "_cs-username",
    "destination.port": "_destination.port",
    "dst_port": "_dst_port",
    "eventSource": "_eventSource",
    "EventType": "_EventType",
    "md5": "_md5",
    "payload": "_payload",
    "sha1": "_sha1",
    "sha256": "_sha256",
    "userAgent": "_userAgent",
    "user_agent": "_user_agent",
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
        IPV4: "_ipv4",
        IPV6: "_ipv6"
    },
    "DestinationIp": {
        IPV4: "_ipv4",
        IPV6: "_ipv6"
    },
    "IpAddress": {
        IPV4: "_ipv4",
        IPV6: "_ipv6"
    },
    "IPaddress": {
        IPV4: "_ipv4",
        IPV6: "_ipv6"
    },
    "dst_ip": {
        IPV4: "_ipv4",
        IPV6: "_ipv6"
    },
    "src_ip": {
        IPV4: "_ipv4",
        IPV6: "_ipv6"
    }
}

ip_field_values = set(val for values in ip_field_mapping.values() for value in
                      values.values() for val in value)

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
    **field_mapping, **string_value_field_mapping, **file_and_dir_field_mapping,
    **ip_field_mapping
}