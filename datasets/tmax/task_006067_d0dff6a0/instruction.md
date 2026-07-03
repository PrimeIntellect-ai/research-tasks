You are assisting a Capacity Planner in setting up an automated analysis pipeline to process server resource usage data. You need to write a C++ analyzer, an idempotent build configuration, and a mini-CI/CD bash pipeline that simulates sending mailing-list alerts via a local Maildir structure.

Your objectives are as follows:

1. **C++ Resource Analyzer:**
   Create a C++ program at `/home/user/src/analyzer.cpp`. 
   The program should take a single command-line argument: the path to a CSV file.
   The CSV file (which will be at `/home/user/resource_usage.csv`) has no header and contains three comma-separated columns: `Timestamp (string), CPU_Percentage (int), Memory_Percentage (int)`.
   The program must read the file and compute:
   - The average CPU percentage (integer division is fine).
   - The maximum Memory percentage.
   
   If the average CPU percentage is strictly greater than 75, print `ALERT_CPU_HIGH` on a new line.
   If the maximum Memory percentage is strictly greater than 85, print `ALERT_MEM_HIGH` on a new line.
   Print nothing else.

2. **Idempotent Build (Makefile):**
   Create a `/home/user/src/Makefile`. 
   It should have a default target that compiles `analyzer.cpp` into an executable located at `/home/user/bin/analyzer`. 
   Ensure it creates the `/home/user/bin/` directory if it does not exist. 
   The compilation must be idempotent (running `make` twice should not recompile if the source hasn't changed).

3. **Maildir Setup and Pipeline Script:**
   Create a bash script at `/home/user/pipeline.sh`.
   When executed, this script must perform the following tasks:
   a. Create a standard Maildir directory structure at `/home/user/alerts_mail/` (this means creating `/home/user/alerts_mail/new/`, `/home/user/alerts_mail/cur/`, and `/home/user/alerts_mail/tmp/`).
   b. Invoke `make` in the `/home/user/src/` directory to build the analyzer.
   c. Run `/home/user/bin/analyzer /home/user/resource_usage.csv` and capture its output.
   d. If the analyzer outputs *any* alerts (i.e., output is not empty), the script must generate an email file inside `/home/user/alerts_mail/new/` named exactly `latest_alert.msg`.
   e. The email file MUST have the following exact format:
      ```
      To: capacity-team@local.domain
      From: planner-bot@local.domain
      Subject: Capacity Alert

      <Insert the exact output of the analyzer here>
      ```

Ensure that your `pipeline.sh` script is executable. You do not need to run the pipeline yourself, but it must be fully functional when invoked.