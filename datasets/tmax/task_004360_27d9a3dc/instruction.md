You are an incident responder investigating a potentially compromised Linux server. We have identified a suspicious compiled Python executable file that appears to be syncing data with an external server. It runs as a cron job, but we only have the compiled bytecode.

Your task is to reverse engineer this file and extract the hardcoded credentials and network indicators. 

The suspicious file is located at: `/home/user/worker.pyc`

Perform the following actions:
1. Analyze the `/home/user/worker.pyc` file (you may use Python's built-in `dis` module or standard bash utilities like `strings`).
2. Identify the authorization token being passed as a command-line argument to a subprocess (this token is leaked via `/proc` when the script runs).
3. Identify the target domain name the script is communicating with over HTTPS.
4. Save the exact authorization token to a file named `/home/user/leaked_token.txt`.
5. Save the exact target domain name to a file named `/home/user/target_domain.txt`.

Ensure that both text files contain only the requested string values with no extra spaces or formatting.