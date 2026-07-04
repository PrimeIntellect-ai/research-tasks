You are a cloud architect migrating our legacy services to a new edge infrastructure. We have a Rust-based health-checking agent that needs to be deployed to highly resource-constrained IoT nodes.

Your tasks:
1. **Extract Configuration:** We lost the original text configuration, but a screenshot of the dashboard remains at `/app/target_config.png`. Read the image to find the `TARGET_PORT` and the `SECRET_TOKEN`.
2. **Update Code:** Update the Rust health checker located at `/home/user/health_monitor/src/main.rs`. Modify it so that it connects to `127.0.0.1` on the port you extracted, and sends the secret token as part of its payload (or just prints it, depending on the code structure).
3. **Optimize Binary Size:** Because this binary will run on edge devices, it must be highly optimized for size. Modify `/home/user/health_monitor/Cargo.toml` and use any build commands necessary so that the final compiled binary (`/home/user/health_monitor/target/release/monitor`) is as small as possible. Your goal is to get the binary size under 400,000 bytes.
4. **Fix Execution:** There is a wrapper script at `/home/user/run_monitor.sh` simulating our cron execution. It currently fails to output to the correct directory due to environment path differences. Fix the script so that running it successfully writes the monitor's output to `/home/user/logs/monitor.log`.

Run the script once to generate the log. Do not use root privileges.