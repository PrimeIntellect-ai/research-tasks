You are a network engineer troubleshooting connectivity to a virtualized router endpoint. A custom UDP probing utility is used to measure network throughput to this endpoint, but it is currently underperforming and dropping packets due to a bug in its source code. 

Your task consists of three parts: fixing the probe, achieving the target throughput, and setting up an automated logging and rotation mechanism.

1. **Fix the Vendored Package:**
   You have been provided the source code for the probing utility `fast-udp-probe` (version 1.0) located at `/app/fast-udp-probe-1.0`. 
   Currently, when compiled and run, it achieves an artificially low throughput. Inspect the C source code, identify the deliberate perturbation causing the bottleneck in the packet transmission loop, and fix it. Recompile the package using the provided Makefile.

2. **Achieve the Metric Threshold:**
   Start the simulated router endpoint by running the background service script provided at `/app/router-sim/start_endpoint.sh`. 
   Once the endpoint is listening on UDP port 8080, run your fixed `fast-udp-probe`. 
   The probe takes two arguments: the target IP (use `127.0.0.1`) and the port (`8080`). 
   It will output its final throughput in packets per second (pps). 
   You must pipe or redirect the exact standard output of a successful run (which contains a line formatted as `Throughput: <number> pps`) to `/home/user/results.txt`. 
   Your fixed C program must achieve a throughput of **at least 5000 pps**.

3. **Configure Log Rotation:**
   Create a bash script at `/home/user/monitor.sh` that appends the output of the probe to a log file at `/home/user/probe.log`. 
   Implement a custom log rotation mechanism within this script: before running the probe, if `/home/user/probe.log` exists and its size is greater than 1000 bytes, it should be rotated to `probe.log.1` (and `probe.log.1` to `probe.log.2`, keeping a maximum of 2 backups).

Ensure `/home/user/results.txt` contains your high-throughput result so it can be verified.