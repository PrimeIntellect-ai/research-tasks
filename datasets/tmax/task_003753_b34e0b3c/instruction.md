You are a data analyst tasked with building a real-time log aggregation pipeline using only standard Linux shell tools (Bash, awk, sed, sort, join, etc.). 

We have three internal microservices that emit log data over TCP sockets. 
Currently, the system is configured via a multi-service setup. When `/app/start_services.sh` is executed, it starts three local servers on the following ports:
1. **Port 9001 (Orders)**: Emits CSV data. Format: `YYYY-MM-DD HH:MM:SS, order_id, amount`
2. **Port 9002 (Payments)**: Emits TSV (tab-separated) data. Format: `UnixEpochTimestamp \t order_id \t status`
3. **Port 9003 (Shipping)**: Emits pipe-delimited data. Format: `YYYY-MM-DDTHH:MM:SSZ | order_id | warehouse`

Your task is to write a single Bash script at `/home/user/aggregator.sh` that orchestrates a multi-stage pipeline to:
1. Connect to all three TCP ports simultaneously (e.g., using `nc` or bash `/dev/tcp`) and stream the data.
2. Parse and align all timestamps to standard Unix Epoch seconds.
3. Perform an inner join on `order_id` across all three streams. Only include an `order_id` if it appears in all three streams.
4. Output the aggregated data to standard output (stdout) as a single CSV with the exact format:
   `order_id,unix_timestamp_from_orders,amount,status,warehouse`
5. The final output must be sorted numerically by `unix_timestamp_from_orders` ascending, and then by `order_id` alphabetically.
6. The script should gracefully exit and flush output once the TCP streams close (the servers will close the connection after sending their batch of logs).

Constraints:
- You must use Bash and standard GNU coreutils / awk / sed. Do not write Python, Perl, or other scripts.
- The script must be marked as executable.
- The multi-service environment is already configured in `/app/start_services.sh`.

Write the `/home/user/aggregator.sh` script so that it accurately processes the streams. Your script will be tested against a hidden reference implementation using randomized fuzzy inputs across the sockets to ensure bit-exact equivalence of the output.