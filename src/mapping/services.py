
kql_service_mapping = {
    10: 'apache',
    11: ['auditd', 'clamav', 'cron', 'sshd', 'sudo'],
    12: ['auth', 'powershell', 'sysmon', 'wmi'],
    347: 'cloudtrail',
    449: 'gcp.audit',
    (397, 452, 515): 'threat_management',
    (11, 12): ['rdp', 'smbclient-security', 'syslog', 'taskscheduler'],
    433: 'windefend',
}

first_key = next(iter(kql_service_mapping))  # מקבל את המפתח הראשון
print(type(first_key)) 