You are tasked with setting up an automated alerting and monitoring component for a legacy deployment. As part of a migration, we are replacing a proprietary log-parsing alerting binary with an equivalent Python script.

We have provided a reference implementation of the proprietary parser at `/app/legacy_alert_parser.bin`. This binary takes a single string (a log line) as an argument and outputs a serialized JSON alert object to standard output, or nothing if the log line does not trigger an alert. 

Your goals are:
1. Extract the filtering rules. We lost the original documentation, but a screenshot of the old configuration dashboard is available at `/app/alert_rules_screenshot.png`. You will need to use OCR (e.g., `tesseract`, which is preinstalled) to extract the exact regex and threshold parameters from this image.
2. Create a Python script at `/home/user/new_alert_parser.py` that takes a log line as its first CLI argument.
3. The script must replicate the logic of the legacy binary. It must apply the rules extracted from the image to determine if an alert should be triggered. If it triggers, it must output exactly the same JSON format as the legacy binary.
4. Set up a user-level `systemd` service (`/home/user/.config/systemd/user/alert-watcher.service`) that runs a wrapper script to monitor a log file `/home/user/app.log`. Note: there is a known issue where this service sometimes fails to start on reboot because it depends on a local dummy mail relay service. You must ensure the service file correctly specifies its startup dependencies (it must wait for `dummy-mail-relay.service`). Ensure appropriate read/execute ACLs and permissions are set on the scripts.

The automated testing will fuzz your `/home/user/new_alert_parser.py` against `/app/legacy_alert_parser.bin` with 5000 random log lines to ensure absolute bit-exact equivalence in standard output.