You are a performance engineer working on the core physics engine for a new simulation software. We are currently profiling and validating our numerical integrators against real-world data.

We have a test fixture in the form of a video recording of a 2D damped pendulum experiment located at `/app/pendulum.mp4`. The video runs at 30 frames per second for exactly 10 seconds. In the video, a bright red circular bob swings back and forth against a black background.

However, our current naive Euler integrator diverges rapidly due to a lack of step-size adaptation, rendering our physics engine unstable for stiff or long-running simulations.

Your task is to:
1. **Environment Setup**: Create a Python virtual environment at `/home/user/venv` and install necessary scientific and computer vision packages (e.g., `opencv-python`, `scipy`, `numpy`, `pandas`).
2. **Video Processing**: Extract the $(x, y)$ pixel coordinates of the center of the red bob for each frame in the video.
3. **Parameter Estimation**: The pendulum dynamics can be approximated by the nonlinear ODE: $\theta'' + b \theta' + \frac{g}{L} \sin(\theta) = 0$. Use nonlinear optimization to estimate the effective damping coefficient ($b$) and length ($L$), assuming $g = 9.81$. You will need to convert the $(x, y)$ pixel positions to an angle $\theta$. The pivot of the pendulum is at the top-center of the video frame (x=320, y=0). 100 pixels = 1 meter.
4. **Stable Integration**: Implement a numerically stable Python script `/home/user/simulate.py` that uses an adaptive step-size method (e.g., RK45 or an implicit method) to solve the ODE from $t=0$ to $t=10$ seconds using your estimated $b$ and $L$. The initial conditions $(\theta_0, \theta'_0)$ should be derived from the first few frames of your extracted video data.
5. **Output**: Your script must generate a CSV file at `/home/user/simulation.csv` with exactly three columns: `time`, `theta`, and `theta_dot`. Evaluate the trajectory at precisely 30 FPS intervals (i.e., $t = 0.0, 0.0333..., 0.0666...,$ up to $t=9.966...$).

Your final simulation must accurately match the underlying true physics parameters that generated the video. We will grade your `simulation.csv` by computing the Mean Squared Error (MSE) of your $\theta$ values against the hidden ground-truth mathematical trajectory. A highly stable and accurate integrator will achieve a very low error.