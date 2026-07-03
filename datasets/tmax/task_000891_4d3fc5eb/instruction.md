You are a Site Reliability Engineer responding to a monitoring outage. The legacy health-check signing gateway has crashed, and its source code was lost. The only surviving component is the core signing logic, which exists as a stripped, undocumented binary located at `/app/health_signer`.

Your task is to restore the monitoring infrastructure by completing two objectives: text-processing legacy logs and writing a new multi-protocol health-check gateway in C.

**Objective 1: Log Analysis**
There is a log file at `/home/user/system_health.log` containing recent monitoring pings.
Write a bash script at `/home/user/analyze_logs.sh` that processes this log file. 
The log lines look like this:
`[2023-10-12T10:00:00Z] NODE=app-1 IP=10.0.0.5 STATUS=OFFLINE RESPONSE_TIME=TIMEOUT`
Your script must find all lines where `STATUS=OFFLINE`, extract the IP address and the timestamp (without brackets), and write them space-separated to `/home/user/offline_nodes.txt`.
Example output line: `10.0.0.5 2023-10-12T10:00:00Z`

**Objective 2: Multi-Protocol Gateway (C)**
The uptime monitoring system needs a gateway to generate health signatures. By experimenting with `/app/health_signer`, you will notice it takes exactly two command-line arguments (an IP and a timestamp) and outputs a signature string to stdout.

Write a C program at `/home/user/gateway.c` and compile it to `/home/user/gateway`. The program must run as a daemon (or background process) and simultaneously listen on two ports on `127.0.0.1`:

1.  **Port 8080 (HTTP):**
    *   Accepts `GET /sign?ip=<IP>&time=<TIMESTAMP> HTTP/1.1`
    *   Must spawn `/app/health_signer <IP> <TIMESTAMP>` and read its output.
    *   Must respond with a valid HTTP/1.1 200 OK response containing a JSON body: `{"ip":"<IP>","time":"<TIMESTAMP>","signature":"<SIGNATURE_FROM_BINARY>"}` (where `<SIGNATURE_FROM_BINARY>` has the trailing newline removed).

2.  **Port 8081 (Raw TCP):**
    *   Accepts a single line of text formatted exactly as: `CHECK <IP> <TIMESTAMP>\n`
    *   Must spawn `/app/health_signer <IP> <TIMESTAMP>` and read its output.
    *   Must respond with: `OK <SIGNATURE_FROM_BINARY>\n` and then close the connection.

**Requirements:**
- Use standard C libraries (POSIX). You may use `fork()`, `exec()`, `popen()`, or similar for invoking the binary.
- Ensure the C program gracefully handles multiple sequential requests without crashing.
- Leave the compiled `/home/user/gateway` running in the background when you finish your turn so the automated verifier can test it.