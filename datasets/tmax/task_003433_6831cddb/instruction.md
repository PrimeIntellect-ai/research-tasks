You are an edge computing engineer responsible for deploying a lightweight telemetry aggregator to our new fleet of IoT devices. Due to restricted network access at the edge, you have been provided with the vendored source code for the aggregator package. 

Your objective is to fix the provided package, compile it, and set up a resilient deployment using shell scripting.

**1. Fix and Compile the Telemetry Aggregator**
* The source code for `edgetelem-1.2.0` is located at `/app/edgetelem-1.2.0`.
* Attempt to build it using `make`. You will find that compilation fails, and even if forced, the service fails to bind to the correct port. 
* Identify and fix the deliberate perturbations in the C code:
  * Fix the missing standard library header that causes a compilation error under strict flags.
  * The server is designed to listen on the port specified by the `TELEM_PORT` environment variable. Fix the logic bug in `server.c` that causes it to bind to the wrong port.
* Compile the binary successfully. The resulting executable should be named `edgetelem`.

**2. Configure the Deployment**
* The service must run and listen on `127.0.0.1` on port `8080`.
* The service writes received telemetry to a local file. You must configure it to write to `/home/user/data/telemetry.log` (you may need to create the `data` directory). Check the source code to see how to configure the output path (usually via an environment variable `TELEM_OUT`).

**3. Process Monitoring and Backup Strategy**
Since IoT environments are unstable, you must write a master shell script at `/home/user/edge_deploy.sh` that acts as both a watchdog and a scheduled backup runner.
The script must:
* Run continuously in a loop (e.g., checking every 1 second).
* **Health Check**: Check if the `edgetelem` service is responding on `http://127.0.0.1:8080/ping`. If it is not running or not responding, start or restart the service in the background.
* **Backup**: Check the size of `/home/user/data/telemetry.log`. If it exceeds 100 bytes, move it to `/home/user/backups/telemetry-<timestamp>.bak` (where `<timestamp>` is the current Unix epoch time) and signal the service to recreate the log file (or restart the service if it doesn't support live reloading, to ensure data isn't lost).
* Create the `/home/user/backups/` directory if it doesn't exist.

**Final State**
Start your deployment script in the background: `bash /home/user/edge_deploy.sh &`.
The automated verifier will send HTTP GET requests to `/ping` and HTTP POST requests with JSON payloads to `/submit` on `127.0.0.1:8080`, and verify that backups are properly generated in `/home/user/backups/` when the log grows.