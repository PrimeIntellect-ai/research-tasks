You are acting as a network engineer troubleshooting connectivity for a custom reverse proxy setup. We have a Python-based routing resolver vendored at `/app/proxy-resolver` (version 1.4.0). This package is responsible for deciding which upstream Unix socket a connection should be forwarded to, but it is currently causing 502 Bad Gateway errors because it is calculating the wrong socket paths.

Your tasks are:
1. **Fix the Vendored Package:**
   The package contains a CLI tool `/app/proxy-resolver/resolver.py` that reads lines from standard input in the format `<src_ip> <dst_domain>` and outputs the target socket path on standard output.
   Currently, the routing logic in `/app/proxy-resolver/router.py` is broken. You must fix it so that it adheres to our exact routing specification:
   - Construct a string combining the source IP and destination domain separated by a colon: `<src_ip>:<dst_domain>`
   - Compute the MD5 hash of this string.
   - Extract the LAST two characters of the resulting hex digest.
   - Parse these two characters as a base-16 integer.
   - Compute the modulo 4 of this integer.
   - Return the corresponding socket path: `/var/run/upstream_<result>.sock` (where `<result>` is 0, 1, 2, or 3).
   
2. **CI/CD Pipeline Construction:**
   Write a CI test script at `/home/user/run_ci.sh` that feeds exactly 3 lines of test data into `/app/proxy-resolver/resolver.py` and verifies the output. The script must exit with code 0 if successful, and non-zero otherwise.

3. **Scheduled Task Configuration:**
   Create a crontab file at `/home/user/resolver.cron` that schedules `/home/user/run_ci.sh` to run every 5 minutes. Do not install the crontab, just create the valid configuration file.

Ensure that `/app/proxy-resolver/resolver.py` is executable and outputs exactly one socket path per line of input.