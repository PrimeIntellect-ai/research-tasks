You are tasked with building a Rust-based data processing tool that analyzes a log of server configuration changes. The system currently exports a CSV file containing timestamped configuration updates, but the values often contain embedded newlines which historically caused fragile Bash scripts to silently drop rows. 

Your goal is to write a Rust program that accurately reads this CSV, aggregates the changes into hourly buckets, and reshapes the data to generate a clean Markdown report.

**Task Requirements:**

1. **Setup**: Create a new Rust project named `config_tracker` in `/home/user/`.
2. **Input**: Read the CSV file located at `/home/user/config_changes.csv`. 
   The CSV has the following columns: `timestamp,server_id,config_key,config_value`.
   - `timestamp` is in ISO8601 format (e.g., `2023-10-01T10:15:30Z`).
   - `config_value` may contain embedded newlines enclosed in quotes. You must parse these correctly without dropping rows.
3. **Processing**:
   - Extract the "Hour" bucket from the timestamp (e.g., `2023-10-01T10`).
   - Aggregate the data: Count the number of times each `config_key` was modified per `server_id` within each hourly bucket.
4. **Output Generation**:
   - Generate a Markdown report at `/home/user/hourly_report.md`.
   - The file must exactly follow this template:
     ```markdown
     # Configuration Change Report
     
     ## Hour: {YYYY-MM-DDTHH}
     - {server_id}: {config_key} ({count})
     ```
   - Rules for output ordering:
     - Hours must be sorted chronologically.
     - Within each hour, `server_id`s must be sorted alphabetically.
     - Within each `server_id`, `config_key`s must be sorted alphabetically.
     - Leave exactly one blank line before each `## Hour:` heading. Do not leave trailing whitespace or extra blank lines at the end of the file.

Write the Rust code, build it using Cargo, and run it to produce `/home/user/hourly_report.md`.