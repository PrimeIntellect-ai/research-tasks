You are a data engineer tasked with building an ETL pipeline using only Bash and standard command-line tools (e.g., `awk`, `sed`, `grep`, `sort`, `date`, `iconv`). 

You have been provided with raw server metric logs in the directory `/home/user/incoming/`. The files contain metrics from different server regions but are notoriously messy.

Your objective is to write a script or execute commands to process these files into a clean, normalized, and aggregated output file at `/home/user/etl_output.csv`.

Here are the pipeline requirements:

**1. Character Encoding Handling:**
The files in `/home/user/incoming/` may be in different encodings (e.g., UTF-8, ISO-8859-1). Ensure all data is processed as UTF-8.

**2. Validation (Quality Gate):**
The input files have a header row: `timestamp,region,cpu,mem`.
Filter out any data rows where `cpu` or `mem` are negative values (less than 0). Discard the entire row if any metric is invalid. Also, ensure you do not include the header rows in the final output.

**3. Reshaping (Wide to Long format):**
Convert the valid rows from a wide format into a long format. 
Each input row should produce two rows in the long format, one for the `cpu` metric and one for the `mem` metric.
The temporary fields should be: `timestamp`, `region`, `metric_name`, `metric_value`

**4. Timestamp Alignment:**
Some files use standard Unix epochs (e.g., `1696154400`), while others use formatted datetime strings (e.g., `2023-10-01 10:00:00`). 
Convert all timestamps to Unix epoch integers. Treat all formatted datetime strings as UTC. 

**5. Sorting & Windowed Aggregation:**
Sort the long-format data logically by `region` (ascending), `metric_name` (ascending), and `timestamp` (ascending).
Next, calculate a 2-period rolling average of the `metric_value` partitioned by `region` and `metric_name`. 
* For the first reading of a specific region and metric, the rolling average is just the value itself.
* For subsequent readings, the rolling average is the mean of the *current* and *immediately previous* `metric_value`.
Format the rolling average to exactly one decimal place (e.g., `55.0`, `55.5`).

**Final Output Format:**
Write the results to `/home/user/etl_output.csv`.
The file should have no header row.
The columns must be comma-separated in this exact order:
`unix_epoch,region,metric_name,original_metric_value,rolling_avg_2`

*Note: You must only use Bash shell built-ins, coreutils, and standard Unix CLI tools. No Python, Perl, or Ruby allowed.*