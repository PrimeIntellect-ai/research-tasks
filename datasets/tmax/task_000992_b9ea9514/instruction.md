You are tasked with porting a legacy security policy updater to run inside a minimal container environment. The tool applies security updates to policy files and reports the changes to an audit server over WebSockets.

Currently, the minimal container lacks standard high-level libraries, so you must implement the core logic in a C program.

Your objective is to create a C program at `/home/user/updater.c` that performs the following steps:

1. **Calculate Initial Checksum:**
   Read the existing security policy file located at `/home/user/policy.conf`. Calculate its Fletcher-16 checksum. 
   *Fletcher-16 Algorithm for this task:* 
   Initialize `sum1 = 0` and `sum2 = 0`. For each byte `b` in the file:
   `sum1 = (sum1 + b) % 255`
   `sum2 = (sum2 + sum1) % 255`
   The final checksum is an integer: `(sum2 << 8) | sum1`.

2. **Apply Patch:**
   Apply the unified diff file located at `/home/user/update.patch` to `/home/user/policy.conf`. You may use the system `patch` utility by invoking it via `system()` or `popen()` within your C code.

3. **Calculate Final Checksum:**
   Re-read the updated `/home/user/policy.conf` and calculate its new Fletcher-16 checksum using the exact same algorithm.

4. **WebSocket Communication:**
   A local WebSocket audit server is running on `ws://127.0.0.1:8080`. 
   Have your C program send a single JSON message to this WebSocket server in the following format:
   `{"status": "patched", "old_checksum": 1234, "new_checksum": 5678}`
   (Replace `1234` and `5678` with the actual integer checksums you calculated).
   *Hint:* Since you are in a minimal environment, you may use the pre-installed command-line tool `websocat` (e.g., executing `echo '<json>' | websocat ws://127.0.0.1:8080`) from within your C program to handle the WebSocket framing.

**Setup Instructions:**
Before running your C program, you must start the provided audit server. A simple Python WebSocket server script is located at `/home/user/ws_server.py`. 
Start it in the background: `python3 /home/user/ws_server.py &`
This server will listen on port 8080 and append all received messages to `/home/user/audit_log.json`.

Compile your program to `/home/user/updater` using `gcc` and run it. Do not hardcode the checksums; your C program must calculate them dynamically.