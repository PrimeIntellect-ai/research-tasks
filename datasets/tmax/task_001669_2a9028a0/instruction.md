You are acting as a capacity planner and system administrator debugging a misconfigured network monitoring setup. The previous administrator left behind an architecture diagram as an image and a set of raw network logs, but the automatic filtering system is broken.

Your task has multiple stages:

1. **Extract Configurations from Image**
   There is an architecture diagram at `/app/topology_diagram.png`. Use `tesseract` (which is preinstalled) or another vision tool to extract the text from this image. It contains three critical pieces of information for the capacity planner:
   - `SUBNET`: The allowed internal subnet CIDR.
   - `RESTRICTED_PORT`: A port that should never receive external traffic.
   - `QUOTA_MB`: The maximum allowed size for a log file payload.

2. **Develop the Network Log Classifier**
   Write a Python script at `/home/user/classifier.py`. This script must act as a CLI filter for network logs.
   - It should accept exactly one argument: the path to a JSON log file.
   - The JSON files contain dictionaries with keys: `source_ip` (string), `dest_port` (integer), and `log_size_mb` (float).
   - The script must evaluate the JSON against the rules extracted from the image.
   - A log is considered "Clean" (Compliant) ONLY IF:
     a) `source_ip` is strictly within the allowed `SUBNET`.
     b) `dest_port` is NOT the `RESTRICTED_PORT`.
     c) `log_size_mb` is strictly less than or equal to `QUOTA_MB`.
   - The script must `exit(0)` if the log is clean, and `exit(1)` if it violates any rule (evil).
   
   To help you develop and test your script, we have provided two directories of sample logs:
   - `/app/corpus/clean/` (All files here should result in exit code 0)
   - `/app/corpus/evil/` (All files here should result in exit code 1)

3. **System Configuration Management**
   - Create a directory `/home/user/configs/available/` and `/home/user/configs/enabled/`.
   - Create a JSON configuration file at `/home/user/configs/available/network_rules.json` containing the rules you extracted from the image (keys: `subnet`, `restricted_port`, `quota_mb`).
   - Create a symbolic link at `/home/user/configs/enabled/active.json` pointing to `/home/user/configs/available/network_rules.json`.

4. **Service Lifecycle**
   - Create a user-level systemd service named `log-analyzer.service` located in the correct directory for user systemd services (`~/.config/systemd/user/`).
   - The service should have a `[Service]` block with `ExecStart=/usr/bin/python3 /home/user/classifier.py /home/user/configs/enabled/active.json` (even though active.json isn't a standard log, this simulates the daemon's start command).
   - Reload the user systemd daemon and enable the service so it is recognized. (You do not need to successfully start it, just enable it).

Ensure your Python script is robust, as it will be evaluated against a hidden, strictly graded adversarial test suite of clean and evil JSON logs formatted identically to the provided corpora.