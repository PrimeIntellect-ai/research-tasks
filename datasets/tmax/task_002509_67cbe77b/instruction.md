You are a performance engineer tasked with profiling and stabilizing a numerical simulation service. We have a legacy C-based numerical integrator that simulates a nonlinear damped oscillator. However, it currently diverges due to incorrect step-size adaptation.

First, locate the system diagram image provided at `/app/system_specs.png`. This image contains a handwritten critical damping coefficient ($\zeta$) and the natural frequency ($\omega_0$) required to stabilize the system. Extract these parameters.

Second, there is a C source file at `/home/user/integrator.c`. You need to compile this scientific software from source into an executable named `/home/user/integrator`. Modify the compilation or wrapper script to pass the extracted $\zeta$ and $\omega_0$ as environment variables (`DAMPING_COEF` and `NATURAL_FREQ`) to ensure numerical stability during execution.

Third, write a Bash script `/home/user/analyze.sh` that takes the output of the integrator (a time-series of displacement values), performs a Fast Fourier Transform (FFT) using Python or a provided utility, and prints the dominant frequency. You must use an optimization routine (like gradient descent or simple grid search) within your Bash/Python scripts to find the optimal maximum step size (`H_MAX`) that minimizes the difference between the theoretical natural frequency (from the image) and the simulated dominant frequency.

Finally, you must expose this stabilized integration and spectral analysis pipeline as a network service. Bring up an HTTP server listening on `127.0.0.1:8080`. 
- The server must accept a `POST` request at the `/simulate` endpoint.
- The request body will be JSON containing a `duration` field (e.g., `{"duration": 10.5}`).
- The server must run the optimized integrator for that duration, run the spectral analysis, and return a JSON response containing the optimized step size and the dominant frequency: `{"h_max": <float>, "dominant_frequency": <float>}`.
- The server must require a Bearer token for authentication. The token is `perf-eng-token-2024`. Reject unauthorized requests with a 401 status.

Ensure your service is running and bound to the specified port so it can be verified.