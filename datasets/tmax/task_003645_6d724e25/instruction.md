You are a FinOps analyst tasked with automating the retrieval, deployment, and notification of daily cloud cost reports. You need to pull data from a legacy interactive billing tool, deploy it to a local web server using a staged deployment logic, and send an email notification. 

Perform the following tasks using Bash and related tools:

1. **Automated Data Retrieval (Expect Scripting):**
   There is a legacy CLI tool located at `/home/user/bin/legacy_billing`. When executed, it interactively prompts for:
   - `Username:` (You must provide: `finops`)
   - `Password:` (You must provide: `CostCut2024!`)
   
   Write an Expect script named `/home/user/fetch_costs.exp` that automates this interaction. The script must capture the JSON output of the legacy tool and save it strictly to `/home/user/staging/report.json`.

2. **Staged Deployment:**
   Create a deployment bash script at `/home/user/deploy.sh`. This script should:
   - Run the `/home/user/fetch_costs.exp` script to generate the staging report.
   - Parse `/home/user/staging/report.json` to extract the value of the `total_cost` field.
   - Implement a simple deployment gate: If `total_cost` is less than or equal to `5000`, copy the file to `/home/user/prod/report.json`. If it is greater than `5000`, do NOT copy it to prod. Ensure `deploy.sh` has executable permissions.
   - Run the script so the file is deployed to production.

3. **Web Server Setup:**
   Serve the `/home/user/prod/` directory via a local HTTP web server listening on port `8080`. Start this server in the background so it remains running. 

4. **Email Notification:**
   A local mock SMTP server is already running on `127.0.0.1` at port `1025` (it requires no authentication or TLS). 
   Write a bash command or script to send an email through this local SMTP server with:
   - **Sender**: `finops@localhost`
   - **Recipient**: `cfo@example.com`
   - **Subject**: `Cost Report Deployed`
   - **Body**: `The latest cost report has been deployed to the web server.`

Ensure all scripts are executed and the web server is running when you finish.