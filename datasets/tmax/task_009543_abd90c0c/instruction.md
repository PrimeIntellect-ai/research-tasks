You are a system administrator tasked with building a monitoring script that alerts on low disk space and reports the server's default gateway.

We have gathered the server's state into two mock text files:
1. `/home/user/disk_usage.txt` (simulated output of `df -m`)
2. `/home/user/routes.txt` (simulated output of `ip route`)

Your task is to write a text processing pipeline and a C++ program to generate an alert log.

Step 1: Write a C++ program
Create `/home/user/report_builder.cpp` and compile it to an executable `/home/user/report_builder`.
The program must read from standard input (`std::cin`).
- The first line of standard input will be the default gateway IP address.
- The subsequent lines will be the names of filesystems (e.g., `/dev/sda1`) that are critically full (one per line).
- The program must write an alert log to `/home/user/alert.log` with the exact following format:
```
GATEWAY: <ip>
WARNING_FS: <fs1>, <fs2>, ...
```
- The filesystems in `WARNING_FS` must be comma-separated with a space after the comma, in the exact order they were received.
- If no filesystems are provided in the input, it should output `WARNING_FS: NONE`.

Step 2: Write a Shell Script
Create an executable bash script `/home/user/process.sh` that does the following:
1. Extracts the IP address of the default gateway from `/home/user/routes.txt`. The default gateway is on the line starting with "default via", and the IP is the next word.
2. Extracts the names of the filesystems (the first column) from `/home/user/disk_usage.txt` where the `Use%` (the fifth column) is 80% or higher. Skip the header row.
3. Pipes this data into `./report_builder` such that the default gateway IP is the first line of input, and the filesystem names follow on subsequent lines.

Step 3: Run the Script
Execute `/home/user/process.sh` so that it successfully generates `/home/user/alert.log`.