You are an operations engineer triaging intermittent crashes in our legacy, in-memory timeseries database service. The service is a C++ TCP server that handles metric ingestion and time synchronization. Recently, the service crashed violently, and we managed to capture a core dump. We need you to figure out what killed it, prove it, and replace the service.

The legacy binary (stripped of debug symbols) is located at `/app/legacy_ts_db`.
The core dump from the production crash is located at `/app/crash.core`.

Your objectives are:

1. **Memory Dump Analysis**: Analyze the core dump to find the exact network payload (the final command) that caused the service to crash. The service uses a text-based TCP protocol, and the offending payload is a string ending in a newline (`\n`). 

2. **Intermittent Failure Reproduction**: Write a C++ regression test client at `/home/user/reproducer.cpp`. This client should compile to `/home/user/reproducer`, connect to `127.0.0.1:9000`, and send the exact payload you discovered in the core dump. We will use this to verify the vulnerability.

3. **Convergence Failure Repair (Write a Replacement)**: The legacy binary is beyond saving. Write a new C++ server from scratch at `/home/user/ts_server.cpp` (compile to `/home/user/ts_server`). Your server must listen on TCP `127.0.0.1:9000` and implement the following line-based, synchronous protocol:
   - `PUT <key> <unix_timestamp> <float_value>\n` -> Stores the metric and responds with `OK\n`.
   - `GET <key> <unix_timestamp>\n` -> Responds with `VAL <float_value>\n` if found, or `NOT_FOUND\n` if not.
   - `SYNC <timezone_offset>\n` -> This is the command that crashed the old server due to a 32-bit integer overflow bug on extreme offsets. Your new server must safely process this offset by calculating the remainder when divided by `86400` (the number of seconds in a day) using standard C++ `%` semantics. It must respond with `OK <remainder>\n`. For example, `SYNC -86405\n` should return `OK -5\n`.

Ensure your server runs continuously in the foreground once started and handles multiple sequential requests gracefully (you do not need to support concurrent connections, just a single persistent connection that processes multiple commands). Keep the in-memory store simple. 

Compile your new server and leave it running in the background on port `9000` when you are finished.