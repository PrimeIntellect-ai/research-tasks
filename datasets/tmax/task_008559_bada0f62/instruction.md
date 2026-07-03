You are tasked with fixing and processing a dataset from a configuration management system that tracks server settings over time. Recently, the ETL job that collects these logs experienced connection retries, causing exact duplicate records to be inserted into the raw logs. Furthermore, some corrupted log lines were written.

You need to analyze the logs to find security regressions—specifically, whenever a server's `SSH_ROOT_LOGIN` configuration was changed from `no` to `yes`. 

Here is what you need to do:

1. **Read and Validate Data**: Process the file `/home/user/raw_configs.log`. Extract the timestamp, server ID, IP address, config key, and config value. You must use regex to parse the lines and ignore any lines that do not strictly match this format:
   `[YYYY-MM-DD HH:MM:SS] <server_id> <ip_address> <CONFIG_KEY>=<value>`
   *(Note: Any line with a malformed timestamp or missing fields should be discarded.)*

2. **Deduplicate**: Because of the ETL retry bug, there are exact duplicate log entries. Ensure you remove duplicate entries so that you have only one record per unique combination of timestamp, server_id, and configuration state.

3. **Filter Environments**: You are only interested in production servers. Join your parsed logs with `/home/user/server_meta.csv` to filter and keep only records for servers where the `environment` is `prod`.

4. **Detect Changepoints**: For each production server, process its configurations in chronological order. Identify the exact timestamp when the `SSH_ROOT_LOGIN` configuration transitions *from* `no` *to* `yes`. (If a server starts as `yes`, or changes from `yes` to `no`, that is not a regression. We only want `no` -> `yes` transitions).

5. **Generate Output**: Create a CSV file at `/home/user/changepoints.csv` with exactly two columns: `server_id` and `change_timestamp`. 
   - The file must include a header: `server_id,change_timestamp`.
   - The rows must be sorted alphabetically by `server_id`.
   - If a server has multiple regressions, output only the *first* time it transitioned from `no` to `yes`.

You may use any programming language (e.g., Python, Bash, Perl, etc.) available in a standard Linux environment to write your processing script.