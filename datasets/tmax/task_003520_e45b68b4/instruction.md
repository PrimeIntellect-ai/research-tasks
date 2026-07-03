You are a support engineer tasked with running a diagnostic collection script on a failing system. The system's diagnostic tool is located at `/home/user/diag-tool/`. However, the tool is currently broken and misconfigured.

Your goal is to fix the script, find the correct configuration values, and successfully generate the final diagnostic report.

Here is what you need to do:

1. **Fix the Bash Bug:** The script `/home/user/diag-tool/collect.sh` is supposed to concatenate all log files in `/home/user/logs/` into a single file. However, it currently fails to read some log files because their filenames contain spaces. Modify `collect.sh` so that it correctly handles filenames with spaces.

2. **Pcap Analysis:** The service was trying to communicate with a specific local port, but the connection was refused. Analyze the packet capture file located at `/home/user/capture.pcap`. Identify the destination TCP port number that the client attempted to connect to (which received a connection refused / RST packet).

3. **Git Forensics:** The script requires an API secret to run, which was accidentally hardcoded into the `diag-tool` repository in the past, but later removed. Recover this secret from the git repository's commit history located at `/home/user/diag-tool/`.

4. **Configuration:** Update the `/home/user/diag-tool/.env` file. Replace the placeholder values with the port number you found in the pcap file and the secret you recovered from the git repository.

5. **Generate the Report:** Run the fixed `/home/user/diag-tool/collect.sh` script. If everything is correct, it will generate a final report at `/home/user/report.json`.

Ensure that the final output file `/home/user/report.json` is generated and contains the correct configuration values.