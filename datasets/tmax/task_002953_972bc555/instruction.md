You are an edge computing engineer tasked with resolving a critical deployment failure on our new batch of IoT sensor hubs. After a recent OTA update, the nodes are silently rejecting key-based SSH logins due to corrupted dynamic ACL generation. 

We have isolated the problem to two areas: a failing legacy binary that generates these ACLs, and a disk storage runaway issue that is filling up the telemetry partitions.

Your objectives are as follows:

**Phase 1: Diagnostic Extraction (Video)**
The field team recorded the boot sequence of the failing IoT hub, which displays a diagnostic hexadecimal seed on-screen right before the disk error occurs. The video is located at `/app/boot_diagnostic.mp4`. 
1. Use `ffmpeg` to extract the frames and find the exact 8-character hexadecimal diagnostic seed. It appears as an overlay text in the video exactly when the screen flashes red.
2. Save this exact 8-character string to `/home/user/diagnostic_seed.txt`.

**Phase 2: Storage Automation & Alerting**
The IoT hub's storage directory at `/home/user/telemetry_data/` is prone to filling up. 
1. Create a bash script at `/home/user/monitor_storage.sh` that checks the total size of `/home/user/telemetry_data/`.
2. If the directory exceeds 50 Megabytes, the script must delete the oldest files until the directory is under 40 Megabytes.
3. If files were deleted, the script must append an alert message formatted exactly as `ALERT: Storage cleanup executed at [Unix Timestamp]` to `/home/user/admin_alerts.mbox` (acting as a local mail spool for our alerting agent).
4. Configure a scheduled task (using the user's `crontab`) to run this script every 5 minutes.

**Phase 3: ACL Compiler Replacement (Go)**
The proprietary binary `/app/bin/legacy_acl_compiler` is responsible for reading raw incoming sensor payloads (from stdin) and outputting an SSH configuration snippet (to stdout) that allows key-based login for authorized maintenance devices while rejecting others. The legacy binary is unstable, but we need its exact output format.
1. Write a replacement program in Go at `/home/user/acl_compiler.go`.
2. Your Go program must read a stream of bytes from `stdin`. 
3. For every incoming payload, it must behave *exactly* identically to `/app/bin/legacy_acl_compiler`. You should execute the legacy binary with various test inputs to reverse-engineer its behavior.
4. Note: The legacy binary's behavior involves XORing the input with the diagnostic seed you extracted in Phase 1, and then wrapping the hex-encoded result in an SSH `Match User iot_admin` block containing an `AuthorizedKeysFile` directive.
5. Compile your Go program to `/home/user/acl_compiler`. Our automated verification will heavily fuzz your compiled binary against the legacy oracle to ensure bit-exact equivalence for any input payload.

Ensure all file paths, permissions (executable bits on scripts), and expected output formats match exactly. You have standard user access. Do not attempt to use `sudo`.