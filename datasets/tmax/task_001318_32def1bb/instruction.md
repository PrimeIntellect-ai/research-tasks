You are tasked with a critical forensics and debugging investigation for a long-running service. 

We have a proprietary, stripped binary located at `/app/telemetry_daemon`. Recently, this service has been crashing due to out-of-memory (OOM) errors. We suspect a memory leak is being triggered by specific corrupted or maliciously crafted telemetry packets received over the network. 

To help you investigate, we have provided:
1. `/app/telemetry_daemon`: The stripped executable. It processes a single binary telemetry payload passed via standard input (e.g., `/app/telemetry_daemon < payload.bin`).
2. `/app/traffic.pcap`: A network capture containing a mix of valid and corrupted packets sent to the daemon.
3. `/app/daemon_state.wal`: A recovered, partially corrupted Write-Ahead Log from the local SQLite database that the daemon uses to buffer payloads.

Your goal is to:
1. Extract the payloads from the PCAP and/or WAL.
2. Use tools like `valgrind` and delta debugging techniques against `/app/telemetry_daemon` to identify the exact binary pattern/encoding anomaly causing the memory leak.
3. Write a C program located at `/home/user/filter.c` and compile it to `/home/user/filter`.

**Filter Specification:**
The program `/home/user/filter` must take a file path as its first CLI argument. It must read the binary payload from the file and determine if it will trigger the memory leak in the daemon.
- If the payload is SAFE (will not cause a leak), the program must exit with status code `0`.
- If the payload is UNSAFE (contains the structural anomaly that triggers the leak), the program must exit with status code `1`.

Note: The daemon uses a custom Type-Length-Value (TLV) encoding. You will need to reverse-engineer the minimum packet structure required to parse the packets and identify the corrupted state handling that leads to the leak.