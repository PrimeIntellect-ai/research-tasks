You are a capacity planner building a local telemetry system to monitor disk storage. You have a partially completed setup that consists of a metrics server, a C++ disk monitor, and a bash-based process supervisor. Currently, the system fails to run reliably because the C++ service crashes on startup due to a missing dependency check (it tries to connect to the server before the server port is open), and the C++ code itself is incomplete.

Your goal is to complete the C++ implementation, fix the process supervisor, and wrap it all in a mock CI/CD pipeline script.

System Components:
1. **Metrics Server**: A pre-existing Python script at `/home/user/metrics_server.py`. It simulates a slow-starting service (takes ~2 seconds to initialize) and then listens on `127.0.0.1:9090` for TCP connections. When it receives a message, it logs it to `/home/user/server.log`.
2. **Data Directory**: `/home/user/data/` contains various logs and files whose total size needs to be monitored.
3. **Capacity Planner (C++)**: `/home/user/capacity_planner.cpp` is a partially written C++ program. 
4. **Supervisor Script**: `/home/user/supervisor.sh` starts the server and the C++ binary.

Your Tasks:

**1. Complete the C++ Program**
Edit `/home/user/capacity_planner.cpp`. You must add the missing logic to:
- Recursively calculate the total size (in bytes) of all files in `/home/user/data`.
- Connect to the metrics server at `127.0.0.1` port `9090` via TCP.
- Send the calculated size in the exact format: `CAPACITY:<total_bytes>\n`
- If the connection fails, the program must exit with a non-zero status code.

**2. Fix the Process Supervisor**
Edit `/home/user/supervisor.sh`. Currently, it starts the Python server and immediately starts the compiled C++ binary, causing the C++ binary to fail. You must:
- Add a connectivity diagnostic (e.g., using `nc` or bash `/dev/tcp`) to wait until port `9090` is actively accepting connections before launching the C++ binary (mimicking a systemd `After=` dependency).
- Add a simple restart policy for the C++ binary: if it crashes or exits with a non-zero code, the supervisor should restart it (up to a maximum of 3 attempts).

**3. Build the CI/CD Pipeline**
Create a script at `/home/user/ci_pipeline.sh` (ensure it is executable) that performs the following steps:
- Compiles the `/home/user/capacity_planner.cpp` into an executable named `/home/user/capacity_planner`. Use `g++ -std=c++17`.
- Executes `/home/user/supervisor.sh`.
- Monitors `/home/user/server.log`. Once a line starting with `CAPACITY:` appears, the pipeline should print "PIPELINE SUCCESS", cleanly terminate the background processes spawned by the supervisor, and exit with code 0.
- If it takes longer than 15 seconds, it should print "PIPELINE TIMEOUT", kill the processes, and exit with code 1.

Ensure all file paths used are absolute. Do not use root or `sudo`.