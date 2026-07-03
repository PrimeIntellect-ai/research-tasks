You are an incident responder investigating a recent web server compromise. The attacker managed to wipe most of their tracks, but they accidentally left behind a screenshot of their scanning tool's configuration at `/app/scan_config.png`.

We need to build a robust intrusion detection filter to scan our archived web logs and identify which servers were targeted by this specific tool. 

Your task:
1. Extract the hidden configuration details from `/app/scan_config.png`. Tesseract is installed on the system. You are looking for a unique `User-Agent` string or a specific URL payload pattern used by the attacker's tool.
2. Based on the extracted information, write a Bash script at `/home/user/detect.sh` that acts as a log classifier.
3. The script must take exactly one argument: the path to a web access log file.
4. The script should analyze the log file. If the file contains ANY entries matching the attacker's specific pattern (derived from the image), the script must print exactly the word `MALICIOUS` to standard output and exit.
5. If the file does not contain the attacker's pattern, it must print exactly the word `CLEAN` to standard output and exit.

Ensure your script is executable (`chmod +x /home/user/detect.sh`). It will be evaluated against a corpus of clean and malicious log files.