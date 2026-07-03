You are an observability engineer tasked with tuning our monitoring pipeline and protecting our dashboard from log injection attacks. We have a multi-service pipeline running in `/home/user/app/` consisting of:
1. A lightweight QEMU VM that generates raw system logs and sends them over a virtual network interface (`tap0`) via UDP to port 5000.
2. A fast log filter service, which you must write in C, listening on UDP port 5000, filtering the logs, and forwarding the safe ones via TCP to our dashboard service on port 8080.
3. A dashboard service (Python HTTP server) listening on TCP port 8080 that ingests clean logs.

Your task is to write the C filter program (`/home/user/workspace/log_filter.c`) that acts as a strict sanitiser. It must compile to `/home/user/workspace/log_filter` and run as a daemon.

The C filter must:
1. Bind to UDP `127.0.0.1:5000` to receive logs from the QEMU VM.
2. Parse each log line. A log line is considered "clean" if it matches standard syslog formats and contains no control characters (other than `\n`), no shell metacharacters (e.g., `|`, `>`, `<`, `&`, `;`, `$`), and no excessively long words (over 100 characters). It is considered "evil" if it violates these rules.
3. Forward "clean" log lines to the dashboard service by connecting to TCP `127.0.0.1:8080` and sending the line.
4. Discard "evil" log lines.
5. Additionally, implement a command-line mode for bulk testing: when invoked as `./log_filter --test <input_file> <output_file>`, it should read lines from `<input_file>`, and write only the "clean" lines to `<output_file>`, discarding the "evil" ones.

We have provided a corpus of logs to help you tune your filter:
- `/home/user/corpus/clean/`: Contains files with known safe logs.
- `/home/user/corpus/evil/`: Contains files with malicious log injection attempts.

To complete the task:
1. Write the `log_filter.c` source code.
2. Compile it using `gcc -O2 -o /home/user/workspace/log_filter /home/user/workspace/log_filter.c`.
3. Configure the network routing to ensure the QEMU VM can reach UDP port 5000 on the host (the startup scripts in `/home/user/app/start_services.sh` will launch QEMU and the dashboard, but you need to ensure the routing on `tap0` is correct and your filter is running).
4. Start your filter service.

The verifier will test your `./log_filter --test` implementation against a hidden validation corpus and will verify the end-to-end flow from the QEMU VM to the dashboard.