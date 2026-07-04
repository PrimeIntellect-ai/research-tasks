You are a cloud architect migrating our edge routing filter to a new user-space simulated environment. The legacy setup relied on systemd, but our new deployment uses shell-based supervisors. 

Currently, our local environment setup is broken. The main entry point, `/home/user/startup.sh`, attempts to initialize the environment and start the simulated services. However, the downstream simulated router consistently crashes on boot because it tries to read the routing rules before the initialization step completes—a race condition analogous to a missing `After=` dependency in systemd. 

Your task consists of three phases:

**Phase 1: Environment & Script Fixes**
1. Modify `/home/user/startup.sh` so that it correctly sequences the execution. Ensure that the initialization script (`/home/user/init_routing.sh`) completes fully *before* any background simulated services are launched. 
2. The script must be fully idempotent.
3. Ensure that the startup script properly exports the environment variables `TZ=UTC` and `LC_ALL=C`.
4. Fix the file permissions on `/home/user/routing_rules/` so that only the owner has read, write, and execute access (ACL equivalent to 0700).

**Phase 2: Legacy Telemetry Extraction**
The actual routing rules for the new filter are encoded in a legacy video recording of our old network dashboard, located at `/app/legacy_dashboard.mp4`.
- The video is exactly 60 seconds long at 1 FPS (60 frames total).
- Each frame corresponds to a routing zone, from Zone 1 (frame 0) to Zone 60 (frame 59).
- Extract the frames using `ffmpeg`. Analyze the exact center pixel of each frame (resolution is 640x480, so center is x=320, y=240). 
- If the center pixel's Red channel is strictly greater than 128, that Zone is considered "ACTIVE". Otherwise, it is "INACTIVE".
- Store this boolean mapping of active zones; you will hardcode or load it into your Rust application.

**Phase 3: Rust Filter Implementation**
Write a Rust application in `/home/user/router_migrator/`. 
1. The application must read line by line from `stdin`. Each line will contain an IPv4 address string (e.g., `10.15.2.100`).
2. The application must determine the "Zone" of the IP by inspecting its second octet. For example, `10.15.2.100` belongs to Zone 15.
3. If the zone is between 1 and 60 (inclusive), check if the zone is ACTIVE based on your video analysis. 
4. If the zone is ACTIVE, the output should be `[<TZ>|<LC_ALL>] FORWARD <IP>`. (Substitute `<TZ>` and `<LC_ALL>` with the values from the environment variables).
5. If the zone is INACTIVE, or if the second octet is outside the 1-60 range, the output should be `[<TZ>|<LC_ALL>] DROP <IP>`.
6. Compile the binary in release mode. The final executable must be located at `/home/user/router_migrator/target/release/router_migrator`.

The output of your Rust program must be bit-exact equivalent to our internal oracle. Do not include any extra logging on stdout. Make sure you use standard tools (bash, coreutils, ffmpeg, rustc/cargo) available in the environment.