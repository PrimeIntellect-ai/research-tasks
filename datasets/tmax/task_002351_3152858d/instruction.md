As an automation specialist, you are tasked with standardizing and analyzing mixed-format server logs. 

I have a file at `/home/user/raw_logs.txt` that contains log entries from various microservices. However, due to a migration, the file contains a mix of two formats:
1. Comma-separated values (CSV): `timestamp,service_name,status_code`
2. JSON: `{"timestamp": "...", "service": "...", "status": ...}`

Your task is to write a Bash script at `/home/user/process_logs.sh` (make sure it's executable) that processes this file and creates a normalized output file at `/home/user/processed_logs.csv` meeting the following requirements:

1. **Multi-format parsing**: Extract the timestamp, service name, and status code from both formats.
2. **Quality gate**: Discard any log entries where the `status_code` is not a strictly 3-digit integer (e.g., discard lines with "ERROR", "None", or "20").
3. **Sorting and Grouping**: Order the entries primarily by `service_name` (alphabetical ascending) and secondarily by `timestamp` (chronological ascending).
4. **Windowed Aggregation**: For each service, calculate a rolling average of the `status_code` over a sliding window of the last 3 valid requests (the current request and the up to 2 immediately preceding it for that specific service). 
    * If a service has fewer than 3 requests at a given point, calculate the average of the available requests.
    * Use integer division (floor) for the average calculation.

The final output file `/home/user/processed_logs.csv` must be a CSV file with the following headers (as the first line), followed by the processed data:
`timestamp,service,status,rolling_avg`

You may use standard Linux command-line tools (bash, awk, sed, grep, sort, jq, etc.). 
Execute your script to generate the final output file before completing the task.