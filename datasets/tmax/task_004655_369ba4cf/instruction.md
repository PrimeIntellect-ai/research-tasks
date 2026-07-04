You are a system administrator tasked with deploying and monitoring a legacy internal web service. The deployment process currently relies on a manual, interactive configuration wizard, which you need to automate as part of a mini CI/CD pipeline.

You have been provided with two files in your home directory (`/home/user`):
1. `/home/user/config_wizard.py`: An interactive Python script that prompts the user for configuration values and generates an `app.conf` file.
2. `/home/user/server.py`: The actual web server that reads `app.conf` and starts an HTTP listener.

Your objective is to fully automate the deployment and write a health check monitor.

Step 1: Write an automation script `/home/user/deploy_pipeline.py`.
This script must:
- Programmatically interact with `/home/user/config_wizard.py`. It should expect the prompts and provide the following inputs:
  - For the "Environment Name:" prompt, provide: `production`
  - For the "Port Number:" prompt, provide: `8123`
- After the configuration wizard completes successfully (creating `app.conf`), the pipeline script must start `/home/user/server.py` as a background process so it continues running after the pipeline script exits.

Step 2: Write a health check script `/home/user/monitor.py`.
This script must:
- Make an HTTP GET request to `http://localhost:8123/status`.
- Parse the JSON response. The server will return a payload like `{"status": "ok", "environment": "production"}`.
- Write a log entry to `/home/user/deployment_status.log` with the exact format:
  `[HEALTHY] Service running on port 8123 in production mode`
  (Replace "8123" and "production" with the actual values dynamically parsed from the JSON response or the configuration, though they should match the expected deployed values).

Step 3: Execution
- Run your `/home/user/deploy_pipeline.py` script.
- Wait a couple of seconds for the server to start.
- Run your `/home/user/monitor.py` script.

Leave the server running in the background when you are finished. Ensure `/home/user/deployment_status.log` is created and contains the correct string.