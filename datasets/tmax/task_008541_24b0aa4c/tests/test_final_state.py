# test_final_state.py
import os
import json
import re
from datetime import datetime

REPORT_PATH = '/home/user/workspace/compliance_report.json'
APP_PATH = '/home/user/workspace/auth_service/app.py'
ACCESS_LOG_PATH = '/home/user/workspace/logs/access.log'
AUTH_JSON_PATH = '/home/user/workspace/logs/auth.json'

def get_expected_brute_force_ip():
    # Parse access.log
    access_failures = []
    with open(ACCESS_LOG_PATH, 'r') as f:
        for line in f:
            # e.g. 192.168.1.55 - - [10/Oct/2023:14:02:10 +0000] "POST /login HTTP/1.1" 401 120
            match = re.match(r'^(\S+).*?\[(.*?)\].*?"[^"]+"\s+401\s+', line)
            if match:
                ip = match.group(1)
                time_str = match.group(2)
                dt = datetime.strptime(time_str, '%d/%b/%Y:%H:%M:%S %z')
                access_failures.append((ip, dt))

    # Parse auth.json
    auth_failures = []
    with open(AUTH_JSON_PATH, 'r') as f:
        for line in f:
            if not line.strip():
                continue
            data = json.loads(line)
            if data.get('status') == 'failed':
                ip = data.get('ip')
                time_str = data.get('timestamp')
                dt = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%SZ')
                # Add UTC timezone info to match access.log
                from datetime import timezone
                dt = dt.replace(tzinfo=timezone.utc)
                auth_failures.append((ip, dt))

    # Correlate
    correlated = []
    for a_ip, a_dt in access_failures:
        for au_ip, au_dt in auth_failures:
            if a_ip == au_ip and a_dt == au_dt:
                correlated.append((a_ip, a_dt))
                break

    # Find IP with > 3 failures in 60 seconds
    ip_times = {}
    for ip, dt in correlated:
        ip_times.setdefault(ip, []).append(dt)

    for ip, times in ip_times.items():
        times.sort()
        for i in range(len(times)):
            count = 1
            for j in range(i + 1, len(times)):
                if (times[j] - times[i]).total_seconds() <= 60:
                    count += 1
            if count > 3:
                return ip
    return None

def get_expected_app_config():
    with open(APP_PATH, 'r') as f:
        content = f.read()

    audit_receipt = None
    match_receipt = re.search(r'"audit_receipt":\s*"([^"]+)"', content)
    if match_receipt:
        audit_receipt = match_receipt.group(1)

    secure_flag = False
    if re.search(r'secure\s*=\s*True', content, re.IGNORECASE):
        secure_flag = True

    httponly_flag = False
    if re.search(r'httponly\s*=\s*True', content, re.IGNORECASE):
        httponly_flag = True

    return audit_receipt, secure_flag, httponly_flag

def test_compliance_report_exists():
    assert os.path.isfile(REPORT_PATH), f"The compliance report is missing at {REPORT_PATH}."

def test_compliance_report_contents():
    with open(REPORT_PATH, 'r') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {REPORT_PATH} does not contain valid JSON.")

    expected_ip = get_expected_brute_force_ip()
    expected_receipt, expected_secure, expected_httponly = get_expected_app_config()

    assert "brute_force_ip" in report, "Missing 'brute_force_ip' in compliance report."
    assert report["brute_force_ip"] == expected_ip, f"Expected brute_force_ip to be {expected_ip}, got {report['brute_force_ip']}."

    assert "cookie_secure_flag" in report, "Missing 'cookie_secure_flag' in compliance report."
    assert report["cookie_secure_flag"] is expected_secure, f"Expected cookie_secure_flag to be {expected_secure}, got {report['cookie_secure_flag']}."

    assert "cookie_httponly_flag" in report, "Missing 'cookie_httponly_flag' in compliance report."
    assert report["cookie_httponly_flag"] is expected_httponly, f"Expected cookie_httponly_flag to be {expected_httponly}, got {report['cookie_httponly_flag']}."

    assert "audit_receipt" in report, "Missing 'audit_receipt' in compliance report."
    assert report["audit_receipt"] == expected_receipt, f"Expected audit_receipt to be {expected_receipt}, got {report['audit_receipt']}."