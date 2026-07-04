Hello! I am a researcher studying the dynamics of a damped harmonic oscillator. I have recorded a video of a red pendulum bob swinging, but my numerical simulation of the system is failing and I need your help to fix the simulation, find the correct damping coefficient, and serve the results.

Here is the setup:
1. **Experimental Data (/app/pendulum_experiment.mp4):**
   This video (30 fps) shows a red circular bob on a white background, swinging back and forth. 
   - Write a script using `ffmpeg` and Python (OpenCV is available) to extract the frames and track the X-coordinate of the center of the red bob over time. 
   - Normalize the extracted X-coordinates so the maximum initial displacement is exactly 1.0. This is your "reference dataset".

2. **Simulation Code (/home/user/sim_project/):**
   I have written a C++ simulation for the ODE $x''(t) + c x'(t) + k x(t) = 0$ (where $k=9.81$). The code uses an adaptive-step Runge-Kutta (RK45) integrator. However, it currently diverges because the step-size adaptation logic in `integrator.cpp` is implemented incorrectly (the error estimate calculation and step acceptance criteria are flawed). 
   - Fix the C++ step-size adaptation so the solver converges accurately.
   - Compile the simulation. The executable should take the damping coefficient $c$ as a command-line argument and output the simulated trajectory (time and position) to standard out or a file.

3. **Orchestration & Convergence:**
   - Write a Python orchestrator (e.g., `orchestrator.py`) that iteratively runs your compiled C++ simulation with different values of the damping coefficient $c$ (between 0.0 and 1.0).
   - Compare the simulated X-trajectory to the reference dataset extracted from the video (using interpolation to match the 30 fps timestamps).
   - Find the optimal damping coefficient $c$ (to two decimal places) that minimizes the Mean Squared Error against the video dataset.

4. **Results Service:**
   - Once the optimal $c$ is found, bring up a persistent HTTP web service on `127.0.0.1:8050`.
   - The service must expose a `GET /api/best_fit` endpoint.
   - It must require an `X-Auth-Token: physics-2024` header.
   - It should return a JSON response in the exact format:
     `{"optimal_c": 0.25, "mse": 0.0012, "datapoints_compared": 300}` (use your actual computed values).

Please leave the HTTP service running in the background as your final step.