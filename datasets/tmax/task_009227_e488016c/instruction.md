We have a local log processing pipeline that works well in our development environment using a slow bash/awk script, but it is failing in CI due to performance timeouts when processing large, out-of-order log files. The script merges logs from multiple servers, sorts them, and applies strict rate-limiting.

To fix the CI failures, you must translate this logic into a high-performance C utility.

Write a C program at `/home/user/log_processor.c` that does the following:
1. Takes two file paths as command-line arguments (e.g., `./log_processor /home/user/server1.log /home/user/server2.log`).
2. Reads both log files. Each line in the log files follows the exact format: `[TIMESTAMP] [IP_ADDRESS] [ACTION]`
   - `TIMESTAMP` is a UNIX timestamp (long integer).
   - `IP_ADDRESS` is an IPv4 address string (e.g., "10.0.0.1").
   - `ACTION` is an uppercase alphanumeric string without spaces.
   - The fields are separated by a single space.
3. Merges the logs and sorts them chronologically (ascending) by `TIMESTAMP`.
   - If timestamps are equal, sort alphabetically by `IP_ADDRESS`.
   - If both timestamps and IP addresses are equal, sort alphabetically by `ACTION`.
4. Filters the sorted entries by applying a rate limit: an IP address is only allowed to perform an action if the timestamp is *strictly greater* than the timestamp of that IP's most recently allowed action. (i.e., `current_timestamp > last_allowed_timestamp`).
   - If an entry violates this rule (meaning `current_timestamp <= last_allowed_timestamp`), drop the log line completely.
5. Writes the final filtered and sorted output to `/home/user/processed.log` in the exact same format (`[TIMESTAMP] [IP_ADDRESS] [ACTION]\n`).

Once you have written the C code, compile it using:
`gcc -O3 /home/user/log_processor.c -o /home/user/log_processor`

Finally, test your program by running it against the two provided log files:
`/home/user/server1.log` and `/home/user/server2.log`.
The program must successfully generate `/home/user/processed.log` matching the rules.