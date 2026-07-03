You are a monitoring specialist tasked with building a robust log alerting and forwarder pipeline for a hypervisor node running QEMU VMs. You need to implement an anomaly detection classifier in Go, integrate it with a log rotation strategy, and wire up multiple background services.

### Part 1: Go Alert Classifier (Adversarial Corpus)
We need a strict log classifier written in Go. Create a source file at `/home/user/classifier.go` and compile it to `/home/user/classifier`.
The tool must accept exactly one argument (the path to a log file):
`./classifier /path/to/logfile.log`

It must read the file and print exactly `EVIL` to stdout and exit with code 1 if ANY of the following threat signatures are detected, otherwise print exactly `CLEAN` to stdout and exit with code 0:
1. **QEMU Monitor Escape:** The log contains the hex sequence `01 63` (which is the Ctrl-A 'c' escape) on one line, and the immediately following line contains the string `system_reset` or `quit`.
2. **OOM Killer Targeting SSH:** A line matches the pattern: `Out of memory: Killed process <any digits> (sshd)`.
3. **Buffer Overflow Payload:** Any line contains a continuous string of 16 or more uppercase 'A' characters represented in hex (i.e., `41` repeated 16 or more times consecutively: `41414141414141414141414141414141`).

To help you develop this, we have provided two directories containing log snippets:
- `/home/user/corpus/clean/`: Contains 20 safe log samples.
- `/home/user/corpus/evil/`: Contains 20 malicious log samples matching the signatures.
Your classifier must score 100% accuracy on these samples.

### Part 2: Multi-Service Compose and Log Rotation
There is a multi-service mock environment managed by a script at `/app/start_services.sh` (this script is already running in the background). It manages:
- **Service A (Log Generator):** Continuously writes fake QEMU serial logs to `/tmp/qemu.log`.
- **Service B (Central Log Aggregator):** Listens on TCP localhost `5000`.

You must:
1. **Forwarding Script:** Create a bash script at `/home/user/forwarder.sh` that continuously tails `/tmp/qemu.log` and streams the output directly to the aggregator on `localhost:5000` using `nc`. Ensure this script runs in the background.
2. **Log Rotation:** Create a logrotate configuration file at `/home/user/qemu-logrotate.conf` that rotates `/tmp/qemu.log`.
   - The log must be rotated when it reaches `1M` in size.
   - Keep 5 backups.
   - Compress old logs.
   - Implement a `prerotate` script inside the logrotate config that runs your compiled `/home/user/classifier` on the log file about to be rotated. If the classifier returns `EVIL`, the prerotate script must copy the suspicious log to `/home/user/backups/quarantine/` (create this directory) before rotation proceeds.

Ensure all scripts are executable and the pipeline is fully functional.