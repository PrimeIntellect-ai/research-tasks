You are a configuration manager tasked with tracking synchronized changes across two critical servers. 

You have been provided with two configuration change logs located at:
1. `/home/user/logs/serverA.log`
2. `/home/user/logs/serverB.log`

Each line in these logs represents a configuration change in the following format:
`[YYYY-MM-DDTHH:MM:SSZ] KEY=VALUE`

Your task is to:
1. Write a C++ program located at `/home/user/tracker.cpp` that parses both log files.
2. The program must perform timestamp alignment: find all timestamps that appear in *both* log files.
3. For these matching timestamps, perform feature extraction by extracting the configuration key (the string between `] ` and `=`) from both files.
4. The C++ program must output these synchronized changes to `/home/user/aligned_features.csv` with the exact header `Timestamp,KeyA,KeyB` followed by the aligned data rows.
5. Compile and run your C++ program.
6. Finally, simulate a local-remote data transfer by creating a gzip-compressed tarball of the CSV file named `sync_data.tar.gz` and moving it to `/home/user/remote_archive/sync_data.tar.gz`.

Ensure your C++ code is robust enough to handle the specified format. The output CSV must not contain spaces after the commas.