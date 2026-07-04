You are assisting a computational physics researcher in building an automated data pipeline for a real-time sensor simulation. 

Currently, the cluster runs a raw simulation data emitter. A background script (`/app/start_services.sh`) brings up this simulation service, which listens on a raw TCP socket at `localhost:9001`. Whenever a client connects to this port, the service streams exactly 1024 lines of CSV data representing a noisy signal over time (format: `time,value`, with a time step of dt = 0.01 seconds) and then closes the connection.

Your task is to build a middleware API using **Bash** that processes this data on demand. 

You must create a Bash script located at `/home/user/middleware.sh` that acts as an HTTP server listening on `127.0.0.1:8080`. You may use tools like `nc` (netcat) or `socat` to handle the socket connections within your Bash script, and you may write auxiliary Python or awk scripts to perform the math, but the core HTTP server and orchestration must be in Bash.

When your Bash service receives an `HTTP GET /analyze` request, it must:
1. Connect to the simulation service at `127.0.0.1:9001` and download the 1024 samples.
2. Perform a Spectral Analysis (FFT) on the `value` column to find the dominant frequency (the frequency with the highest magnitude, excluding the DC component/0 Hz).
3. Compute a 95% Bootstrap Confidence Interval for the **mean** of the `value` column using exactly 1000 resampling iterations.
4. Validate the numerical stability of your results. Round the dominant frequency to 1 decimal place, and the confidence interval bounds to 2 decimal places.
5. Respond to the HTTP request with a valid `HTTP/1.1 200 OK` header, `Content-Type: application/json`, and a JSON body with exactly this format:
   `{"dominant_freq": <float>, "ci_lower": <float>, "ci_upper": <float>}`

For any other HTTP routes (e.g., `/`), your server should return an `HTTP/1.1 404 Not Found`.

**Constraints:**
- Your service must be persistent (able to handle multiple sequential requests).
- You do not need to implement complex HTTP parsing; checking if the first line of the request contains `GET /analyze` is sufficient.
- Ensure your Bash script is executable (`chmod +x /home/user/middleware.sh`) and run it in the background before declaring the task complete.
- The simulation service is already running. You can test your logic by manually connecting to `localhost:9001`.