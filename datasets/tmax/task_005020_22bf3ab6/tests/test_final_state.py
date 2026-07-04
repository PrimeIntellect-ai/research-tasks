# test_final_state.py
import os
import re

def test_final_state():
    metrics_log = "/home/user/metrics.log"
    alerts_path = "/home/user/mail_spool/alerts.txt"
    actions_path = "/home/user/supervisor_actions.sh"

    assert os.path.isfile(metrics_log), f"{metrics_log} is missing."
    assert os.path.isfile(alerts_path), f"Output file {alerts_path} is missing."
    assert os.path.isfile(actions_path), f"Output file {actions_path} is missing."

    # Parse metrics.log to determine expected services exceeding quota
    exceeding_services = []
    with open(metrics_log, "r") as f:
        for line in f:
            match = re.search(r"SERVICE=(\S+)\s+USAGE=(\d+)\s+QUOTA=(\d+)", line)
            if match:
                service = match.group(1)
                usage = int(match.group(2))
                quota = int(match.group(3))
                if usage > quota:
                    exceeding_services.append((service, usage, quota))

    # Verify alerts.txt
    with open(alerts_path, "r") as f:
        alerts_content = f.read().strip()

    expected_alerts = []
    for service, usage, quota in exceeding_services:
        alert_block = (
            f"To: sre-alerts@company.local\n"
            f"Subject: Quota Exceeded for {service}\n"
            f"Body: Service {service} used {usage} bytes, exceeding quota of {quota} bytes."
        )
        expected_alerts.append(alert_block)

    expected_alerts_str = "\n\n".join(expected_alerts)

    # Normalize line endings and spacing for loose comparison
    norm_actual_alerts = re.sub(r'\n{3,}', '\n\n', alerts_content).strip()

    assert expected_alerts_str in norm_actual_alerts or norm_actual_alerts == expected_alerts_str, \
        f"Contents of {alerts_path} do not match the expected format and data.\nExpected:\n{expected_alerts_str}\n\nActual:\n{alerts_content}"

    # Verify supervisor_actions.sh
    with open(actions_path, "r") as f:
        actions_content = f.read().strip()

    expected_actions = [f"supervisorctl restart {service}" for service, _, _ in exceeding_services]
    expected_actions_str = "\n".join(expected_actions)

    assert actions_content == expected_actions_str, \
        f"Contents of {actions_path} do not match the expected commands.\nExpected:\n{expected_actions_str}\n\nActual:\n{actions_content}"