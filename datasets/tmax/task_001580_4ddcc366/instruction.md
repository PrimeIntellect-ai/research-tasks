You are a Machine Learning Engineer preparing a training dataset of spectral and energy features for a new predictive model. You have a legacy, compiled binary `/app/sensor_model` that simulates our proprietary sensor. Unfortunately, the original source code is lost, and the binary has been stripped of symbols.

Your task is to create a C++ service that wraps this legacy simulator, performs convergence testing, and extracts key features for the ML pipeline.

Write a C++ TCP server listening on `127.0.0.1:8888`. 
When a client connects, it will send a single line terminated by a newline (`\n`) in the format:
`ANALYZE <f0> <damping> <target_error>`
(e.g., `ANALYZE 2.5 0.1 0.005`)

For each request, your server must:
1. **Convergence Testing:** Execute the legacy binary iteratively to find the largest time step `dt`. Start with `dt = 0.1` and halve it in each successive iteration (0.1, 0.05, 0.025, etc.). You have reached convergence when the absolute difference in the total signal energy computed between the current `dt` and the immediately previous `dt` is strictly less than `<target_error>`. (For the very first step `dt=0.1`, just compute the energy and proceed to `dt=0.05`).
2. **Numerical Integration:** The binary is called as `/app/sensor_model <f0> <damping> <dt>`. It prints lines containing `t` and `y(t)` separated by a space. Calculate the total signal energy as the numerical integral of $y(t)^2$ over the entire output duration using the Trapezoidal rule.
3. **Spectral Analysis:** Once convergence is reached, compute the dominant frequency (in Hz) of the signal at the converged `dt` using a Discrete Fourier Transform. The dominant frequency is the positive frequency bin (excluding DC, i.e., > 0 Hz) with the highest magnitude.
4. **Response:** Send a single newline-terminated string back to the client in the format:
`RESULT <converged_dt> <energy> <dominant_freq>`
Format all floating-point numbers to exactly 4 decimal places. After sending the response, cleanly close the client connection but keep the server running to accept future requests.

You may use standard C++ libraries. Do not use external libraries (e.g., Boost or FFTW) unless they are natively available in standard Linux toolchains, as you must compile your server using `g++` without installing new packages.

Once your server is ready, compile it to `/home/user/ml_server` and run it in the background so that it is listening on port 8888.