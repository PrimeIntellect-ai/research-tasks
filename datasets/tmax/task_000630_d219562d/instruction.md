You are a Site Reliability Engineer (SRE) investigating a bizarre cascading failure. Our log processing pipeline went down, and we suspect malicious or malformed log payloads are causing infinite loops in our C++ log ingestion service. Additionally, we have a screen recording of the monitoring dashboard during the outage, and fragmented logs across multiple services.

Your objective is to complete the following multi-stage forensics and debugging workflow:

1. **Dependency Resolution:**
   The C++ log parsing project located at `/home/user/log_pipeline/` fails to compile due to a dependency conflict between `fmt` and `spdlog` versions in the `CMakeLists.txt`. Resolve the conflict so the project compiles successfully via `mkdir build && cd build && cmake .. && make`.

2. **Video Forensics & Timeline Reconstruction:**
   During the outage, a diagnostic camera recorded the main SRE dashboard. The video is located at `/app/dashboard_cam.mp4`. 
   - Use `ffmpeg` or any other tool to analyze the video. The dashboard screen turns completely RED (the RGB values of the video become overwhelmingly red) exactly when the master node fails.
   - Find the exact second (timestamp) this happens.
   - In `/home/user/logs/`, you will find `service_a.log`, `service_b.log`, and `service_c.log`. Reconstruct a unified, chronologically sorted log file from these three files, but ONLY include log entries from the exact minute the screen turned red (e.g., if it turned red at 00:01:15, include all logs from 00:01:00 to 00:01:59).
   - Save this reconstructed timeline to `/home/user/reconstructed_timeline.log`.

3. **Recursion Fixing & Adversarial Filter (Sanitizer):**
   The source code in `/home/user/log_pipeline/src/parser.cpp` contains a recursive function `parse_payload()` that enters an infinite loop when encountering specific malformed log sequences (e.g., circular reference tokens).
   - Debug and fix the infinite recursion bug in the C++ code.
   - Implement a filter executable named `sanitizer` (built into `/home/user/log_pipeline/build/sanitizer`).
   - The `sanitizer` must read a single log payload from standard input.
   - It must exit with code `0` if the payload is safe (clean) and valid.
   - It must exit with code `1` if the payload is malformed, contains circular references, or is otherwise designed to trigger the recursion bug (evil).
   - Write regression tests if needed to ensure your fix works.

Ensure your `sanitizer` binary is robust. It will be automatically tested against two hidden corpora of payloads.