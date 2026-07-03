You are an incident responder investigating a compromised machine. A suspicious, undocumented service has been left running locally on port `13337`. 

You have acquired a snapshot of the service's access logs, located at `/home/user/traffic.log`. The log entries are formatted as JSON lines and contain information about the requests made to the service, including the HTTP method, path, response status, headers, and cookies.

Your investigation indicates that the attacker successfully accessed a restricted endpoint at `/admin/flag` to steal data. Most attempts in the log were rejected with HTTP 403 Forbidden, but exactly one request was successful (HTTP 200 OK).

Your task is to:
1. Parse `/home/user/traffic.log` to identify the specific custom headers, user-agent, and cookies used in the successful (status 200) request.
2. Write a Python script named `/home/user/retrieve.py` that uses the `urllib` or `requests` library to reproduce this exact successful request against `http://localhost:13337/admin/flag`.
3. The script must execute the request and write the raw text response (the hidden flag) to `/home/user/evidence.txt`.

Ensure your Python script runs without user interaction and successfully writes the target evidence file.