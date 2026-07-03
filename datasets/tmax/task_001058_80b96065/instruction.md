You are a performance engineer tasked with debugging and deploying a scientific simulation API. 

We have a nonlinear mechanical system simulation. A previous engineer left some audio notes containing the exact calibration parameters (mass `m`, damping `c`, and nonlinear stiffness `k`) needed for the baseline model. The audio file is located at `/app/audio_notes.wav`.

Your tasks are:
1. **Transcribe the audio** to extract the values for `m`, `c`, and `k`. (You may use tools like `ffmpeg` and Python speech recognition libraries).
2. **Compile the sampler**: There is a C source file at `/app/src/mc_sampler.c` which generates Monte Carlo force samples. You must compile it into a shared library (`sampler.so`) that can be called from Python.
3. **Fix the reduction non-determinism**: The provided Python script `/app/src/simulate.py` takes the samples and computes a total energy metric. However, it currently uses standard naive summation across many parallel chunks, leading to non-reproducible results due to floating-point reduction order. You must modify the code to use Kahan summation or Python's `math.fsum` to ensure exact, reproducible floating-point accumulation regardless of chunk ordering.
4. **Solve for equilibrium**: Implement a function using `scipy.optimize.fsolve` to find the steady-state displacement `x` where the nonlinear restoring force `k * x^3 + c * x - F_avg = 0`, where `F_avg` is the deterministic average force from the corrected Monte Carlo samples.
5. **Serve the API**: Create a Python HTTP service (using Flask or FastAPI) listening on `127.0.0.1:8080`.
   - Endpoint: `POST /simulate`
   - Request JSON: `{"seed": <int>, "num_samples": <int>}`
   - Action: Use the compiled C sampler with the given `seed` and `num_samples` to generate forces. Compute the reproducible total energy `E` and the steady-state displacement `x` using the parameters from the audio.
   - Response JSON: `{"energy": <float>, "displacement": <float>}`
   - Authentication: The endpoint must require a bearer token: `Authorization: Bearer sim_token_xyz`

Ensure your API is running in the background so it can be queried.