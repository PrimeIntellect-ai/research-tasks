You are a Site Reliability Engineer investigating a recent outage of a critical virtual machine. You have been provided with the last VNC framebuffer screenshot of the crashed VM and a log of recent network requests. 

Your objective is to build an automated recovery and analysis tool in Rust that performs environment setup, metric calculation, and log management.

Here are the specific requirements:
1. **Error Extraction**: A screenshot of the crashed VM's console is located at `/app/vnc_crash.png`. Use OCR (e.g., `tesseract`, which is preinstalled) to extract the panic code from this image. The image contains a distinct line formatted exactly as `PANIC: 0x<hex_string>`.

2. **Metrics Analysis**: Write a Rust program located in `/home/user/sre_tool` (you must create the cargo project here). The program must read `/app/metrics.log`. Each line in this file follows the format: `timestamp_ms latency_ms status_code`. 
   Calculate the 95th percentile (P95) latency (as a floating-point number) for all requests where the `status_code` is exactly `200`.

3. **Network Configuration**: Within your Rust program, use system commands to automate the following network setup:
   - Create a dummy network interface named `sre-mon`.
   - Bring the `sre-mon` interface up.
   - Add a static route sending traffic for `10.55.0.0/24` through the `sre-mon` interface.

4. **Log Rotation**: Have your Rust program generate a valid `logrotate` configuration file at `/home/user/sre_logrotate.conf`. It should configure rotation for a log file located at `/home/user/sre_tool.log` with the following rules: rotate daily, keep 7 backups, compress old logs, and missing log files should not produce an error.

5. **Output Formatting**: The Rust program must output the final analysis to `/home/user/report.json` in the following exact JSON format:
   ```json
   {
     "panic_code": "<extracted_hex_string_from_image>",
     "p95_latency": <calculated_float_value>
   }
   ```

Ensure your Rust project is fully functional, builds successfully, and writes the required JSON when executed. Do not use root (`su` or `sudo`) for operations unless standard user permissions suffice (the environment allows network configs via standard commands or `sudo` is passwordless if required by the system).