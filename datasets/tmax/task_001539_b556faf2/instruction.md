You are acting as a data scientist analyzing the dynamics of a physical system. 

We have recorded a video of a mechanical system (a damped harmonic oscillator). The video is located at `/app/oscillator.mp4`.
In the video, a white square moves back and forth along the x-axis against a black background. The center of oscillation (the equilibrium point) is at exactly $x = 320$ pixels. The framerate of the video is exactly 30 frames per second.

Your objective is to:
1. Extract the displacement of the white square over time from the video.
2. Fit the extracted displacement data to the standard damped harmonic oscillator ODE:
   d²x/dt² + 2*ζ*ω_n*(dx/dt) + (ω_n)²*x = 0
   to determine the damping ratio (ζ) and the undamped natural frequency (ω_n).
3. Write a C program at `/home/user/ode_solver.c` that solves this ODE analytically or numerically for any given time `t`, initial displacement `x0`, and initial velocity `v0`, using the fixed `ζ` and `ω_n` parameters you found.
4. Compile this C program to an executable at `/home/user/ode_solver`. It should accept arguments as follows: `./ode_solver <x0> <v0> <t>` and output only the final displacement as a floating-point number.
5. Create and run a Python-based HTTP API server listening on `0.0.0.0:8080`.

**API Server Specification:**
*   **Endpoint:** `POST /predict`
*   **Authentication:** The server must require an HTTP header exactly matching: `Authorization: Bearer ODE-FIT-2024`. Reject requests without this with a 401 status code.
*   **Request Payload:** JSON format: `{"t": <float>, "x0": <float>, "v0": <float>}`.
*   **Behavior:** The server must invoke your compiled `/home/user/ode_solver` with the provided parameters and the fitted ζ and ω_n. 
*   **Response:** JSON format: `{"x": <float>}` containing the calculated displacement.

Please leave the HTTP server running in the foreground or background so it can be tested. Put all your setup code, including the server script, in `/home/user/workspace/`.