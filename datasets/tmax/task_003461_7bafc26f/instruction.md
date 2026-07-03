You are an IT support technician investigating a failed nightly job.

The script `/home/user/ticket_system/report_generator.py` aggregates support tickets from a local SQLite database and extracts critical items into a JSON report. However, it crashed last night.

Your task is to debug the script so that it runs successfully and processes **all** records in the database. 

The developer who wrote this left the following notes:
- The database `/home/user/ticket_system/tickets.db` has a `tickets` table.
- Each ticket payload is a JSON string that was base64 encoded and prefixed with the string `"DATA:"`.
- We paginate through the SQLite database in chunks of 10 to save memory.
- The output should be saved automatically by the script to `/home/user/ticket_system/critical_tickets.json` as a JSON array of integers (the ticket IDs).

**Requirements:**
1. Identify and fix the bugs in `/home/user/ticket_system/report_generator.py`. There are at least two distinct logical/boundary errors causing crashes and skipped records.
2. Run the script successfully so that it outputs the correct array of critical ticket IDs to `/home/user/ticket_system/critical_tickets.json`.
3. Do not change the chunk size (batch size) in the script. Fix the root logic errors instead.

Once the JSON file is generated and contains the complete, correct array of critical ticket IDs, your task is complete.