You are a network engineer acting as an incident responder. We suspect one of our internal servers has been compromised via a command injection vulnerability. 

You have been provided with an HTTP access log located at `/home/user/http_requests.log`. The log format is `IP_ADDRESS | HTTP_METHOD | URL`.

Your task involves analyzing this traffic, reversing the delivered payload, and remediating the system changes made by the attacker using standard Bash utilities.

Perform the following steps:
1. Parse `/home/user/http_requests.log` to identify a command injection attempt. The attacker injected a base64-encoded bash payload into the URL.
2. Extract the attacker's IP address and save it to a file named `/home/user/attacker_ip.txt`.
3. Extract the base64-encoded payload from the URL, decode it, and save the exact decoded bash commands to `/home/user/decoded_payload.sh`. Do not execute this malicious script!
4. Analyze the decoded script to understand what the attacker did. The attacker altered the file permissions of a specific configuration directory and dropped a PHP web shell into it.
5. Remediate the damage in that specific directory:
   - Delete the dropped web shell file.
   - Restore the file permissions: all files in that directory must be set to `644`, and all subdirectories must be set to `755`. 

You must accomplish this using only standard Linux CLI tools (Bash, awk, grep, sed, base64, chmod, etc.). Do not write Python or Perl scripts.