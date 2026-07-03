You are a log analyst investigating a potential coordinated slow-loris or brute-force attack on our API gateway. 

You have been provided with an unstructured log file located at `/home/user/auth_gateway.log`. 

Your task is to analyze this log file to find anomalous IP addresses based on their response times and failure rates. You should write a Python script to perform this analysis.

Here are your specific instructions:
1. **Extract Structured Information:** Parse the log file. Each line contains a timestamp, a log level, and a message. The message contains key-value pairs. You need to extract the `IP` address, the `status` of the request (`success` or `failed`), and the `resp_time` (response time in milliseconds, removing the 'ms' suffix).
2. **Anomaly Detection:** We define an "anomalous request" as any request that BOTH failed (`status:failed`) AND took strictly longer than 300 milliseconds (`resp_time > 300`).
3. **Grouping and Sorting:** Group the data by IP address and count the total number of anomalous requests for each IP. 
4. **Reporting:** Sort the IPs descending by their anomaly count. If multiple IPs have the exact same anomaly count, sort them alphabetically by the IP address string to break the tie.
5. **Output:** Extract the top 5 worst offending IPs (those with the highest anomaly counts) and write them to a CSV file located at `/home/user/top_anomalies.csv`. 

The output CSV must have exactly this header: `IP,AnomalyCount` followed by the 5 rows of data.

Example line from the log file:
`2024-03-15T08:00:00Z | INFO | IP:192.168.1.100 action:login status:success resp_time:120ms`

Begin your analysis and ensure the final CSV is correctly formatted and placed at `/home/user/top_anomalies.csv`.