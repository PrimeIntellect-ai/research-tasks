I'm working on a local deployment pipeline and my reverse proxy configuration is failing. We have a lightweight local Nginx configuration designed to act as a gateway for our Python backend, but it currently returns a 502 Bad Gateway error. 

Here is what you need to do:

1. **Fix the Proxy Configuration**: 
   The Nginx config file is located at `/home/user/nginx.conf`. The backend service it proxies to is actually running on port `8080`, but the configuration is currently pointing to the wrong port. Update the `proxy_pass` directive in this file to point to `http://127.0.0.1:8080`.

2. **Create a Pipeline Monitoring Script**:
   Write a Python script at `/home/user/monitor.py` that acts as a mini-CI/CD integration check. The script must:
   - Calculate the disk usage of the `/home/user` directory.
   - Set the timezone to `Asia/Tokyo` (using the appropriate Python standard libraries, no external dependencies like `pytz` are strictly required if using Python 3.9+ `zoneinfo`, but you must output the time correctly).
   - Perform an HTTP GET request to `http://127.0.0.1:8081` (which is where the Nginx gateway listens) and retrieve the HTTP status code. Assume Nginx and the backend are running during the check.
   - Write the results to a JSON log file located at `/home/user/status.json` with the exact following schema:

```json
{
  "timezone": "Asia/Tokyo",
  "timestamp": "YYYY-MM-DDTHH:MM:SS+09:00", 
  "status_code": 200,
  "disk_usage_percent": 15.2
}
```
*Note: `timestamp` should be the current ISO 8601 formatted time in the Asia/Tokyo timezone. `disk_usage_percent` should be a float representing the used percentage of the disk mounted at `/home/user`.*

You do not need to start or reload Nginx yourself; just fix the configuration file and provide the Python monitoring script. Ensure your script is executable (`chmod +x`).