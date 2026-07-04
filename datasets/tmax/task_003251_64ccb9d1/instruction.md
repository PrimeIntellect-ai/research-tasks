You are a system administrator tasked with creating a lightweight network diagnostic logger. Since we cannot install external monitoring agents on this server, you need to write a custom C++ tool that reads network statistics directly from the sysfs virtual filesystem and logs them. 

Please complete the following steps:

1. Simulate some local network traffic to ensure the loopback interface has non-zero statistics. Start a basic Python HTTP server on port 8080 in the background (`python3 -m http.server 8080 &`), and then make at least one successful `curl` request to `http://127.0.0.1:8080`.

2. Write a C++ program at `/home/user/net_monitor.cpp`. This program must:
   - Read the total received bytes from `/sys/class/net/lo/statistics/rx_bytes`.
   - Read the total transmitted bytes from `/sys/class/net/lo/statistics/tx_bytes`.
   - Get the current local time (which will be determined by the `TZ` environment variable).
   - Print the information to standard output in the EXACT following format:
     `[YYYY-MM-DD HH:MM:SS] RX: <rx_bytes> TX: <tx_bytes>`

3. Compile the C++ program using `g++` into an executable named `/home/user/net_monitor`.

4. Execute the compiled program, ensuring that the timezone is explicitly set to `Asia/Tokyo` (using the `TZ` environment variable) during execution. Redirect the standard output of the program to `/home/user/network_log.txt`.

Ensure that the format in `/home/user/network_log.txt` matches the specification exactly and that the RX and TX values are valid integers read from the filesystem.