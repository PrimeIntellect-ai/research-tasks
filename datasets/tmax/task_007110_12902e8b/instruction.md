You are a support engineer investigating a bug in our backend query system. A client reported that a specific query made by the `admin` user failed with a decoding error.

The system consists of a frontend service and a backend C application. 
- The frontend logs requests to `/home/user/logs/frontend.log`.
- The backend logs transactions to `/home/user/logs/backend.log`.
- When the backend encounters a decoding error, it dumps the raw binary query payload to `/home/user/payloads/payload_<tx_id>.bin`.

The backend is written in C (source available at `/home/user/backend.c`). It reads the binary payload, which is supposed to start with a 32-bit integer representing the Query ID. However, the backend is incorrectly reading the Query ID because it performs a raw `fread` into a `uint32_t` on a Little-Endian machine, but the client sends the payload in Big-Endian format.

Your task is to collect diagnostics and create a report file at `/home/user/report.txt` with exactly three lines:
1. The exact timestamp (format: `YYYY-MM-DD HH:MM:SS`) when the `admin` user made their request.
2. The internal Transaction ID (`tx_id`) assigned to this request by the backend.
3. The *corrupted* Query ID (in base-10 decimal) that the C backend incorrectly parsed from the binary payload due to the endianness mismatch.

You must rely strictly on standard shell utilities to inspect the logs, analyze the binary payload, and calculate the corrupted value. Do not modify or compile the C code.