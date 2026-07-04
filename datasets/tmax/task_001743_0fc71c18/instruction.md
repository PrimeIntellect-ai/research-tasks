You are a data engineer tasked with building a lightweight ETL pipeline to safely process and transfer sensitive employee data.

Your objective is to write a Python script and set up a scheduling configuration.

1. **Write the ETL Pipeline (`/home/user/etl.py`)**:
   Create a Python script that performs the following steps in order:
   - **Extract**: Read a CSV file located at `/home/user/raw_data/employees.csv`. The CSV has headers: `id`, `name`, `email`, `ssn`.
   - **Transform (Masking)**: 
     - Replace every `ssn` value completely with the string `XXX-XX-XXXX`.
     - Mask the `email` addresses by replacing everything before the `@` symbol with exactly three asterisks `***` (e.g., `johndoe@example.com` becomes `***@example.com`).
   - **Load**: Save the transformed data as a JSON file (an array of JSON objects) to `/home/user/clean_data/employees_masked.json`.

2. **Scheduling (`/home/user/pipeline.cron`)**:
   Create a cron job file at `/home/user/pipeline.cron` that schedules `/home/user/etl.py` to run using `/usr/bin/python3` exactly at **midnight (00:00) every Sunday**. The cron file should contain exactly one line with the standard cron expression followed by the command.

Ensure you run your Python script once so that `/home/user/clean_data/employees_masked.json` is generated for verification.

Directory constraints:
- Input file path: `/home/user/raw_data/employees.csv`
- Output file path: `/home/user/clean_data/employees_masked.json`
- Assume `/home/user/raw_data/` and `/home/user/clean_data/` already exist.