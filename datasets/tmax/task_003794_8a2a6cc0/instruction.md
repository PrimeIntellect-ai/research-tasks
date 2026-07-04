You are an expert performance engineer and scientific computing developer. We are analyzing a physical system's dampening characteristics from raw experimental video footage, and we need to expose a parameter-fitting service for our researchers.

An experimental video of a 1D damped harmonic oscillator is located at `/app/oscillator.mp4`. The video shows a solid green circle (RGB: 0, 255, 0) moving horizontally on a solid black background at 30 frames per second. 

Your task is to build a high-performance Python HTTP service that fits the unknown parameters of the system using parallel Monte Carlo simulation and adaptive numerical integration.

Follow these requirements exactly:

1. **Video Processing**:
   Write a script to extract the X-coordinate of the center of the green circle for every frame in `/app/oscillator.mp4`. This sequence of X-coordinates represents the true trajectory $x_{true}(t)$ at $t = 0, \frac{1}{30}, \frac{2}{30}, \dots$ seconds.

2. **Numerical Integration**:
   The system follows the ordinary differential equation:
   $1.0 \cdot \ddot{x} + c \cdot \dot{x} + k \cdot x = 0$
   Where $c$ is the damping coefficient and $k$ is the spring constant.
   The initial conditions are $x(0) = x_{true}(0)$ and $\dot{x}(0) = 0$.
   Write a function to simulate this ODE. You must use an adaptive step-size integrator (e.g., `scipy.integrate.solve_ivp` with `RK45`, `rtol=1e-8`, `atol=1e-8`) and perform convergence testing to ensure your step-size adaptation does not diverge over the time domain of the video.

3. **Parallel Monte Carlo Simulation**:
   Implement a parallelized Monte Carlo search across multiple CPU cores to find the optimal parameters. Given $N$ samples, you should sample $c$ uniformly from $[0.1, 2.0]$ and $k$ uniformly from $[10.0, 50.0]$. For each sample, simulate the trajectory and compute the Mean Squared Error (MSE) between the simulated $x(t)$ and the extracted $x_{true}(t)$. You must use Python's `multiprocessing` or `concurrent.futures` to evaluate these samples in parallel.

4. **HTTP Service**:
   Create a FastAPI or Flask application listening on `0.0.0.0:8000`. It must expose the following endpoints:
   * `GET /ping`: Returns `{"status": "ok"}`
   * `GET /trajectory`: Returns the extracted video trajectory as a JSON list of floats: `{"x": [x_0, x_1, x_2, ...]}`
   * `POST /fit`: Accepts a JSON payload `{"num_samples": <integer>}`. It should run the parallel Monte Carlo simulation using the specified number of random samples, find the $(c, k)$ pair with the lowest MSE, and return `{"c": float, "k": float, "mse": float}`.

Start the service in the background and ensure it remains running. Do not use an excessive number of samples by default; let the API payload dictate it.