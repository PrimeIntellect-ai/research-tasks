You are a monitoring specialist tasked with setting up a local alert generation script based on firewall and port-forwarding logs. 

We have a log file located at `/home/user/fw_logs.txt`. 
The log file contains entries in the following format:
`[YYYY-MM-DD HH:MM:SS] <LEVEL>: <MESSAGE> IP:<IP_ADDRESS> PORT:<PORT_NUMBER> - <REASON>`

Your task is to write a robust Python script at `/home/user/generate_alerts.py` that processes this log file and extracts the IP addresses that triggered a specific alert condition.

The alert condition is:
1. The log level is `ERROR`.
2. The message indicates `Port forwarding failed`.
3. The port number is exactly `8080`.

Requirements for your Python script:
1. It must read `/home/user/fw_logs.txt`.
2. It must extract the IP addresses that match the exact alert condition above.
3. It must output the unique extracted IP addresses to `/home/user/alerts.txt`, with one IP address per line, sorted in ascending lexicographical (alphabetical) order.
4. Robustness: If the file `/home/user/fw_logs.txt` does not exist or is completely empty, your script must catch this, simply create an empty `/home/user/alerts.txt` file, and exit with a success (0) status code. Do not crash.

Once you have written the script, execute it so that `/home/user/alerts.txt` is generated based on the current contents of the log file.