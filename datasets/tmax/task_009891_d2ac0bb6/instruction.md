You are an observability engineer tasked with creating a custom C-based metrics exporter to feed into our new dashboard. Since we cannot deploy standard agents on this specific restricted node, you must build a lightweight tool to monitor network routing paths and disk storage quotas.

You need to perform the following steps:

1. Create a working directory at `/home/user/exporter`.

2. Write a C program at `/home/user/exporter/collector.c` that does the following:
   - Simulates reading system network routes by parsing a file located at `/home/user/exporter/mock_route.txt` (assume this file has the exact same format as `/proc/net/route`).
   - Counts the number of active gateway routes. A route is considered a gateway route if its `Flags` column (the 4th column) has the `RTF_GATEWAY` flag set. In `/proc/net/route`, flags are represented as hexadecimal numbers. `RTF_GATEWAY` is `0002`. (Note: The flags field is a bitmask, so you must check if the `0002` bit is set, e.g., `(flags & 0x0002) != 0`). Skip the header line.
   - Reads an integer value from `/home/user/exporter/quota.txt`, which represents the user's disk quota in bytes.
   - Calculates the currently available disk space (in bytes) on the partition hosting `/home/user/exporter` using the `statvfs` system call (available space = `f_bavail * f_frsize`).
   - Writes the gathered metrics to `/home/user/exporter/metrics.prom` in the following exact format (replace bracketed items with the calculated integer values):
     ```
     network_gateway_routes_total {count}
     disk_available_bytes {available}
     disk_quota_bytes {quota}
     ```

3. Compile the C program to an executable named `/home/user/exporter/collector` using `gcc`.

4. Since we don't have root access to use `systemd`, create a bash service lifecycle manager script at `/home/user/exporter/service.sh` that accepts exactly one argument:
   - `start`: Starts the `./collector` executable in the background, writes its PID to `/home/user/exporter/collector.pid`, and exits.
   - `stop`: Reads the PID from `/home/user/exporter/collector.pid`, kills the process, and removes the PID file.

5. Create the mock data files to test your program:
   - Create `/home/user/exporter/quota.txt` containing exactly the number `53687091200`.
   - Create `/home/user/exporter/mock_route.txt` with the following content:
     ```
     Iface	Destination	Gateway 	Flags	RefCnt	Use	Metric	Mask		MTU	Window	IRTT                                                       
     eth0	00000000	010011AC	0003	0	0	100	00000000	0	0	0                                                          
     eth0	000011AC	00000000	0001	0	0	100	0000FFFF	0	0	0                                                          
     eth1	000012AC	020012AC	0007	0	0	100	0000FFFF	0	0	0                                                          
     eth1	000013AC	00000000	0001	0	0	100	0000FFFF	0	0	0
     ```

6. Run `/home/user/exporter/service.sh start`, wait 2 seconds to ensure the metrics file is written, and then run `/home/user/exporter/service.sh stop`. Ensure the output file `/home/user/exporter/metrics.prom` is generated correctly.