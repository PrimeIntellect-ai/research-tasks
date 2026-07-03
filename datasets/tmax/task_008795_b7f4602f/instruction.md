You are acting as a FinOps analyst trying to optimize cloud costs by setting up an automated local reporting pipeline. We need to process a daily cloud cost export, archive the report using a specific directory structure, and format it for our local mailing list server.

You have been provided with a CSV file at `/home/user/cloud_costs.csv` containing raw billing data. 
The CSV has the following headers: `ResourceID,Service,Cost`

Perform the following steps:

1. **Directory Structure & Links:**
   Create a directory structure for archiving reports: `/home/user/reports/archive/`.
   Create a directory for the mailing list outgoing spool: `/home/user/mail_spool/outbox/`.

2. **Data Processing Pipeline (Python):**
   Write and execute a Python script at `/home/user/process_costs.py` that reads `/home/user/cloud_costs.csv`.
   The script must calculate the total cost of only those resources that have a `Cost` strictly greater than 500.00.

3. **Mailing List Configuration:**
   The Python script must generate an email file named `cost_alert.eml` and save it directly into `/home/user/reports/archive/`.
   The file must have the following exact format (replace `<TOTAL>` with the calculated sum, formatted to 2 decimal places):

   ```
   To: finops-list@local.domain
   From: billing-bot@local.domain
   Subject: Daily High Cost Alert
   
   Total high cost: $<TOTAL>
   ```

4. **Final Deployment:**
   Create a symbolic link at `/home/user/reports/latest_alert.eml` that points to `/home/user/reports/archive/cost_alert.eml`.
   Copy the `cost_alert.eml` file into the mailing list spool directory at `/home/user/mail_spool/outbox/cost_alert.eml` so the local mail daemon can pick it up.

Make sure the file permissions allow reading by standard users and that the final directory structure, symlink, and email files match the requirements exactly.