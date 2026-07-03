You are tasked with processing a large volume of configuration change logs to prepare them for a database bulk import. As a configuration manager, tracking changes efficiently across multiple services is critical.

In `/home/user/logs/`, there are multiple log files (`update_01.log`, `update_02.log`, etc.) containing millions of lines of logging data. Interspersed within these logs are configuration change events. 

A configuration change event always looks exactly like this:
`[YYYY-MM-DDTHH:MM:SS] [service-name] CONFIG_UPDATE: <key> changed from '<old_value>' to '<new_value>'`

Your objective is to:
1. Write a C++ program at `/home/user/parser.cpp` that processes all `.log` files in `/home/user/logs/` in **parallel** (e.g., using `std::thread`, `std::async`, or OpenMP).
2. The program should stream the large log files line-by-line rather than loading entire files into memory.
3. Use C++ Regular Expressions (`std::regex`) to extract the timestamp, service name, key, old value, and new value. Note that values may contain spaces, but will not contain single quotes.
4. The program must output the extracted data into a single CSV file at `/home/user/db_import.csv`. The CSV should not have a header row. The columns must be exactly: `timestamp,service,key,old_value,new_value`.
5. Because parallel processing will result in out-of-order writes, you must ensure the final `/home/user/db_import.csv` is sorted chronologically by timestamp. If timestamps are identical, sort alphabetically by service name, then by key. You can sort within your C++ program or use standard Linux utilities on the output file, as long as the final file at `/home/user/db_import.csv` is properly sorted.

Example of a valid log line:
`[2023-10-14T08:30:15] [auth-service] CONFIG_UPDATE: session_timeout changed from '3600' to '7200'`

Expected CSV output line for the above:
`2023-10-14T08:30:15,auth-service,session_timeout,3600,7200`

Requirements:
- Ensure your C++ code is compiled with at least `-std=c++11` or higher.
- Write the final sorted output directly to `/home/user/db_import.csv`.