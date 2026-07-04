You are assisting a capacity planner in analyzing system resource usage. The planner uses a legacy interactive Bash tool that requires specific locale, timezone, and user parameters to generate proper projections. Additionally, this tool relies on a local reverse proxy simulation, managed by a custom launcher script that is currently failing due to an initialization order bug (similar to a missing `After=` dependency in systemd).

Your task is to fix the environment, configure the proxy, and automate the interactive tool using Expect.

Complete the following steps:

1. **Fix the Launcher Dependency:**
   Look at `/home/user/launcher.sh`. It is supposed to start a mock proxy service and then the capacity tool. However, it currently attempts to start the capacity tool *before* the proxy service is ready, causing the capacity tool to crash. 
   Modify `/home/user/launcher.sh` so that `start_proxy` is called *before* `start_capacity_tool`.

2. **Configure the Reverse Proxy:**
   Create an Nginx configuration file at `/home/user/proxy.conf`. The capacity planner needs it to:
   - Run in the foreground (`daemon off;`).
   - Run as an unprivileged configuration (store pid in `/home/user/nginx.pid` and error log in `/home/user/error.log`).
   - Have an `events {}` block (can be empty).
   - Have an `http` block with a `server` block listening on port `8080`.
   - Forward all requests (`location /`) to `http://127.0.0.1:9090`.

3. **Automate the Capacity Tool:**
   The tool `/home/user/capacity_cli` is an interactive script. You need to write an Expect script at `/home/user/generate_report.exp` that executes `/home/user/capacity_cli` and automates the following interactive prompts:
   - When prompted with exactly `Enter Target Timezone: `, supply the value: `America/New_York`
   - When prompted with exactly `Enter System Locale: `, supply the value: `en_US.UTF-8`
   - When prompted with exactly `Enter Planner Username: `, supply the value: `sys_planner`
   - When prompted with exactly `Enter Planner Group: `, supply the value: `capacity_admins`

   The Expect script must capture the final projection output from the tool and save it to `/home/user/capacity_report.txt`. Ensure the expect script waits for EOF so the tool finishes execution.

To succeed, all required files (`launcher.sh`, `proxy.conf`, `generate_report.exp`, and `capacity_report.txt`) must be in `/home/user/` with the exact specified content and formats. You do not need to install Nginx or Expect; assume `expect` is available and `proxy.conf` will be statically verified.