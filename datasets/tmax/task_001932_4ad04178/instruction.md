You are a network engineer troubleshooting a local network monitoring pipeline. The pipeline consists of three services managed by a local `supervisord` instance running in `/home/user/app/`. 

Currently, the monitoring system is highly unstable and extremely slow. You need to fix the process supervision, optimize the text processing logic, and construct a mini CI/deployment script.

Here is the current setup in `/home/user/app/`:
1. `generator.py`: Simulates network traffic by streaming logs to a TCP socket on port 9001.
2. `aggregator.py`: A metrics collection service listening on TCP port 9002. It has an artificial 3-second startup delay before binding to the port.
3. `processor.go`: A Go service that connects to port 9001 (to read logs) and port 9002 (to send metrics).
4. `supervisord.conf`: The configuration file for the process supervisor.

Your tasks are:

1. **Process Supervision & Restart Policy**:
   The `processor` service currently crashes on startup because it attempts to connect to the `aggregator` on port 9002 before the `aggregator` has finished booting. 
   - Modify `/home/user/app/processor.go` to implement a robust connection retry mechanism (a restart/backoff policy) for the connection to port 9002. It should retry at least 5 times with a 1-second delay between attempts.
   - Modify `/home/user/app/supervisord.conf` to ensure `autorestart=true` is set for the processor, and adjust the `priority` values so that the `aggregator` is started before the `processor`.

2. **Text Processing Pipeline Optimization**:
   The `processor.go` service parses incoming log lines in the format: `[TIMESTAMP] SRC_IP DST_IP PROTOCOL BYTES`. It filters for "TCP" and sums the bytes.
   Currently, the processing is extremely slow because it compiles a complex regular expression inside the loop for every single log line. 
   - Optimize the text processing pipeline in `/home/user/app/processor.go` (e.g., by hoisting the regex compilation, using `strings.Split`, or `awk`/`sed`-like string matching logic) so that it processes data rapidly.

3. **CI/CD Pipeline Construction**:
   Write a deployment script at `/home/user/app/deploy.sh` (ensure it is executable) that:
   - Compiles `/home/user/app/processor.go` into an executable named `processor_bin`.
   - Restarts the supervisord services (using `supervisorctl -c /home/user/app/supervisord.conf update` and `supervisorctl -c /home/user/app/supervisord.conf restart all`).

**Verification**:
An automated verifier will evaluate your deployment by running a benchmark script. The verifier will check the metric `logs_per_second` processed by your optimized Go binary. You must achieve a throughput of **at least 50,000 logs per second** to pass.