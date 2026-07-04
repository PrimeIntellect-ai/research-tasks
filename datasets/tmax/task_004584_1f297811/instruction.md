You are an operations engineer triaging a severe incident on a robotic pipeline. A C-based telemetry synchronization tool (`sync_tool`) crashed in production. 

Here is what we know:
1. **The Video**: An incident recording is located at `/app/incident_record.mp4`. The crash in the telemetry parser corresponds to a visual anomaly in the video (a completely solid red frame). You need to extract the frames and find the exact 0-indexed frame number of this anomaly. Save this frame number as a simple integer in `/home/user/crash_frame.txt`.
2. **The Environment**: The binary `/app/sync_tool` and its source `/app/sync_tool.c` are provided. However, running it immediately fails because a custom math library it depends on is "missing". You need to repair this environment misconfiguration (the library is somewhere in `/opt/legacy_libs/`).
3. **The Deleted Data**: The telemetry data file (`run.dat`) that caused the crash was accidentally deleted from the attached loopback filesystem image located at `/app/telemetry.img`. You must inspect the image and recover the deleted plain-text data.
4. **The Bug**: Once you recover the data and run the tool, it will segfault. Use `gdb` or delta debugging to isolate the crash. The program crashes on the edge-case data corresponding to the visual anomaly.
5. **The Algorithmic Fix**: Fix the bug in `/app/sync_tool.c`. Furthermore, the original implementation contains an inefficient $O(N^2)$ algorithm for computing rolling averages over the telemetry array. You must optimize this to $O(N)$ so the program scales to large datasets. 
6. **The Output**: Compile your fixed and optimized C code to `/home/user/fixed_tool`. 

Your goals are to:
- Write the anomaly frame number to `/home/user/crash_frame.txt`.
- Compile the fixed, optimized tool to `/home/user/fixed_tool`.

Your fix will be tested against a massive held-out telemetry file. It must not crash, and it must execute in under 0.2 seconds.