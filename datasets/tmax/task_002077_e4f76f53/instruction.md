As a Site Reliability Engineer (SRE), you are responsible for maintaining a legacy uptime monitoring system. The system's main script is located in a local Git repository at `/home/user/uptime-monitor/`.

Currently, the script `/home/user/uptime-monitor/monitor.sh` parses server log files in `/home/user/logs/` to calculate a weighted uptime score. However, the script is currently failing. On certain days of the month, the bash script crashes during its mathematical calculations, producing incorrect or no results. 

Your tasks are as follows:
1. Investigate and fix the mathematical evaluation bug in `/home/user/uptime-monitor/monitor.sh`. The script must correctly process all valid dates without crashing.
2. The script requires an API key to be passed via the `API_KEY` environment variable. This key was accidentally committed to the Git repository in the past and subsequently removed for security reasons. Use Git history forensics to find this API key and write the exact string to `/home/user/api_key.txt`.
3. After fixing the script and retrieving the API key, run the script against all logs in the logs directory like so: 
   `cd /home/user/uptime-monitor && API_KEY=$(cat /home/user/api_key.txt) ./monitor.sh /home/user/logs/*`
4. Save the final numerical standard output of the successful script execution into `/home/user/final_score.txt`.