You are an engineer tasked with diagnosing a failing deployment pipeline. Our system takes QEMU VM configurations submitted to a local Git repository, validates them, and starts the VMs. Recently, our systemd service `vm-deploy.service` has been crashing during the validation step due to specific malformed network configurations.

We have isolated the issue to a proprietary, stripped validation binary located at `/app/deploy-validator`. It crashes (panics) when processing certain QEMU configuration strings, specifically those with misconfigured network topologies.

Your objectives:
1. **Analyze the Oracle:** Inspect `/app/deploy-validator` and observe its behavior by feeding it QEMU configuration files from two provided directories:
   - `/app/corpus/clean/` (valid configurations that process successfully)
   - `/app/corpus/evil/` (malformed configurations that cause the binary to crash)

2. **Create a Rust Filter:** Write a Rust program that acts as a Git hook helper to intercept these bad configurations before they reach the validator. 
   - Your Rust source code should be in `/home/user/filter_src/`.
   - Compile your program and place the executable exactly at `/home/user/qemu_net_filter`.
   - The program must take a single command-line argument: the path to a QEMU config file.
   - It must exit with code `0` if the configuration is safe (like those in `clean`), and exit with a non-zero code if the configuration is dangerous (like those in `evil`).
   - Your filter must reject 100% of the files in the evil corpus and accept 100% of the files in the clean corpus.

3. **Logging & Rotation:** 
   - Your Rust filter must append a log line to `/home/user/filter.log` for every file processed, formatted exactly as: `[YYYY-MM-DD HH:MM:SS] <FILE_NAME> - <REJECTED/ACCEPTED>`
   - Create a valid `logrotate` configuration file at `/home/user/logrotate.conf` that rotates `/home/user/filter.log` daily, keeps exactly 5 backups, compresses rotated logs, and ensures the file is created with `0644` permissions if missing.

Do not attempt to patch the stripped binary directly. Rely on building the Rust filter to classify the inputs accurately based on the patterns you discover.