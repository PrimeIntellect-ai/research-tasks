You are assisting a physics researcher who is modeling the motion of a specialized damped nonlinear oscillator. 

We have a recorded experiment in a video file located at `/app/oscillator.mp4`. 
The video shows a 640x480 black background with a white square (5x5 pixels) moving horizontally. 
- The video runs at 30 FPS (`dt = 1/30` seconds per frame).
- The center of the frame (x=320) represents the origin `x = 0.0`.
- The scaling factor is 10 pixels = 1.0 unit of distance.
- The y-coordinate is constant and irrelevant.

The motion follows this specific discrete Euler-integration model:
```python
x_{t+1} = x_t + v_t * dt
v_{t+1} = v_t + (-k * x_t - c * v_t) * dt
```
The exact values of the spring constant `k` and damping coefficient `c` are unknown, but they are constant. 

Your tasks:
1. **Video Analysis (Multi-dimensional array manipulation):** Extract the frame-by-frame x-coordinate trajectory of the particle from `/app/oscillator.mp4`. You can use `ffmpeg`, `opencv-python`, or `imageio`.
2. **Optimization:** Use an optimization algorithm (like Nelder-Mead, gradient descent, or differential evolution from `scipy.optimize`) to find the unknown parameters `k` and `c` that best fit the extracted trajectory. 
3. **Simulation:** Write a Python script at `/home/user/simulator.py` that simulates this system.
   - It must accept three arguments: `--x0 <float>` (initial position), `--v0 <float>` (initial velocity), and `--steps <int>` (number of dt steps to simulate).
   - It must use the `k` and `c` values you discovered.
   - It must print ONLY the final `x` position (rounded to 4 decimal places) to standard output.

We have a compiled reference oracle at `/app/oracle_simulator` that predicts the exact final position using the true parameters. Once you have created `/home/user/simulator.py`, we will verify it by fuzzing it against the oracle with hundreds of random initial conditions. Your script's output must be bit-exact equivalent to the oracle's output.