You are a monitoring specialist migrating an old monitoring stack. We have a legacy, closed-source alerting agent located at `/app/legacy_alerter`. This stripped binary evaluates system metrics and determines the alert severity state.

Your objective has two phases: Environment Configuration and Alert Logic Reverse Engineering.

Phase 1: Environment Configuration
1. Start an Nginx reverse proxy running entirely in user-space (without root privileges).
2. The proxy must listen on `127.0.0.1:8080`.
3. It must forward all HTTP requests to a backend alerting dashboard which will eventually run on `127.0.0.1:3000`.
4. Create the Nginx configuration file at `/home/user/nginx_alert.conf` and ensure the proxy is running in the background. Note: you cannot use standard service managers like systemd; run it directly.

Phase 2: Reverse Engineering the Alerter
The binary `/app/legacy_alerter` takes exactly 5 command-line arguments representing system metrics in the following order:
`[CPU_USAGE] [MEMORY_USAGE] [DISK_IO] [NETWORK_TX] [ERROR_RATE]`

Each argument is an integer between 0 and 100.
The binary processes these metrics and outputs a single line to standard output: either `CRITICAL`, `WARNING`, or `OK`.

Since we are migrating away from this unsupported binary, you must reverse-engineer its internal scoring logic. Use tools like `objdump`, `ltrace`, `strace`, `gdb`, or simply treat it as a black box and script a parameter sweep to deduce the formula.

Once you understand the logic, write a Python 3 script at `/home/user/alerter.py` that behaves EXACTLY like the legacy binary. It must accept the same 5 integer arguments via the command line and print the identical severity string to standard output.

Your script will be tested against the legacy binary with thousands of random inputs. Even a single mismatch will cause the verification to fail.