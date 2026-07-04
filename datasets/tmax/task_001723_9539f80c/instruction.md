You are acting as a backup operator testing a critical restore procedure. We recently had a catastrophic failure on our edge routing node, and the deployment scripts and configuration files for our custom Python packet router and health-check monitor were corrupted.

Fortunately, our lead engineer dictated an incident report and recovery parameters before going offline, which was saved as an audio file at `/app/incident_report.wav`. We also have an old, compiled, stripped binary of the routing logic at `/app/oracle_proxy_check` that we managed to recover, but we need the source code recreated in Python to deploy the fixed version.

Your task consists of three phases:

Phase 1: Information Recovery
1. Transcribe the audio file located at `/app/incident_report.wav`.
2. The audio contains the specific base IP address and port offset rules required to route our custom health-check packets. Note these down, as you will need them for the deployment.

Phase 2: Reconstruct the Router Script
Write a Python script at `/home/user/proxy_check.py`. This script must act as our custom network header parser and routing calculator.
It must take exactly one command-line argument: a 16-character hexadecimal string representing a custom network packet header.
The script must parse this header and output exactly one line containing the calculated target IP address and port in the format `IP:PORT`.

The logic (which you must deduce and refine by comparing against `/app/oracle_proxy_check`) involves:
- Using the routing parameters extracted from the audio file.
- Parsing specific bytes of the hex header to calculate IP address octets and the final port.
- Your script's output must be bit-for-bit identical to the output of `/app/oracle_proxy_check` for any valid 16-character hex input. 

Phase 3: Testing and Deployment Setup
1. Ensure your script is executable.
2. Verify that your script matches the oracle's output exactly. The automated deployment system will fuzz your script with thousands of random 16-character hex headers and assert that your script's output matches the oracle's output exactly.

Requirements:
- Do not use root privileges. 
- You may use any available tools (like ffmpeg or whisper if available/installable in user space, or standard Python libraries) to transcribe the audio.
- The final script must be located at `/home/user/proxy_check.py`.