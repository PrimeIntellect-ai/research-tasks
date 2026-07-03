You are an observability engineer tuning the backend dashboard for your company's internal tools. The dashboard relies on a monitoring script that periodically checks the health of various microservices and restarts them if they are down, but the script was accidentally deleted.

Your task is to recreate the health monitor script in Python and use it to restore the system's observability state.

1. First, create a configuration file at `/home/user/app_config.json` with the following exact JSON content:
```json
{
  "services": [
     {"name": "auth_service", "port": 9010, "cmd": "python3 /home/user/mock_auth.py"},
     {"name": "data_service", "port": 9011, "cmd": "python3 /home/user/mock_data.py"}
  ]
}
```

2. Next, create the two mock services:
Create `/home/user/mock_auth.py` with:
```python
import http.server, sys
server = http.server.HTTPServer(('127.0.0.1', 9010), http.server.BaseHTTPRequestHandler)
server.serve_forever()
```
Create `/home/user/mock_data.py` with:
```python
import http.server, sys
server = http.server.HTTPServer(('127.0.0.1', 9011), http.server.BaseHTTPRequestHandler)
server.serve_forever()
```

3. Write a Python script at `/home/user/health_monitor.py` that does the following:
   - Reads `/home/user/app_config.json`.
   - For each service, performs a connectivity diagnostic to check if its TCP `port` on `127.0.0.1` is actively accepting connections.
   - If the port is NOT accepting connections, the script must spawn the service in the background using the specified `cmd` (do not block waiting for it to finish), and log the state as `RESTARTED`. Allow 1 second after spawning for the service to bind to the port.
   - If the port IS accepting connections, log the state as `UP`.
   - Append the results of the checks to `/home/user/status.csv` in the format: `service_name,state`. Process the services in the order they appear in the JSON file.

4. Execute your script twice. Wait 2 seconds between executions. 
   - On the first execution, neither service will be running, so your script should start them and log them as `RESTARTED`.
   - On the second execution, both services should be running, so your script should detect them and log them as `UP`.

When you are finished, `/home/user/status.csv` should contain exactly 4 lines representing the results of the two consecutive runs. Leave the services running in the background.