I need you to help me run a numerical simulation of a nonlinear oscillator and process its spectral properties. I am working on a new dataset but my simulation pipeline is currently broken, and I need a complete bash-driven workflow to fix the simulator, run it, analyze the output, and expose the results via a simple web API.

Here are the requirements:

1. **Fix the Vendored Simulator:** 
   I have a vendored C-based ODE solver package located at `/app/spectral-ode-sim-1.0`. It calculates the time-series of a chaotic dynamical system. However, it currently fails to compile due to a compilation/linking error in its `Makefile`. Identify the issue, fix the `Makefile`, and compile the binary `ode_sim`.

2. **Generate the Simulation Data:**
   Run the compiled `./ode_sim` with the argument `1000` (representing the number of time steps) and redirect its output to `/home/user/sim_results.csv`. The output will be two columns: time and amplitude.

3. **Spectral Analysis & Reference Comparison:**
   Write a Bash script at `/home/user/analyze_and_serve.sh` that orchestrates the following:
   * It should analyze the `/home/user/sim_results.csv` to find the dominant frequency (the frequency with the highest magnitude in its Fourier transform, excluding the DC component at 0 Hz). You may use inline Python within your Bash script to perform the FFT via `numpy` or `scipy`.
   * It must also calculate the dominant frequency for my reference dataset located at `/home/user/reference.csv`.
   * It should evaluate if the dominant frequencies of the two datasets match within a tolerance of `0.05` Hz.

4. **Expose the Results (Multi-Protocol):**
   The `/home/user/analyze_and_serve.sh` script must conclude by starting a persistent HTTP server listening on `0.0.0.0:8333`. 
   When a `GET /status` request is made to this server, it must return an `HTTP 200 OK` response with the `Content-Type: application/json` and a JSON body exactly like this:
   `{"peak_freq": <simulated_peak_frequency_rounded_to_2_decimals>, "reference_match": <true_or_false>}`
   
   *Note: Ensure your server correctly parses the HTTP GET request and sends valid HTTP headers before the JSON body. You can use standard tools like `nc`, `socat`, or Python's `http.server` invoked from within your bash script.*

Please complete the fix, run the data generation, and leave the `analyze_and_serve.sh` script running in the background so the server is up and listening.