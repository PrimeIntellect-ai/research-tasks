You are a data scientist analyzing a video of a chemical experiment to fit a kinetic model. 

We have a video of a reaction at `/app/experiment.mp4`. The video captures a beaker where a red substance (Reactant A) turns into a blue substance (Reactant B), which then turns clear (Product C). 

Your task involves three steps:
1. **Signal Processing (Video Analysis)**:
   Extract the average Red (R) channel intensity for the center 100x100 pixel region of each frame in `/app/experiment.mp4`. Normalize this sequence by dividing by 255.0 to represent the concentration of A over time. Save this 1D time-series data as a comma-separated list of floats in `/home/user/signal.csv`. Assume the video plays at 10 frames per second, so each frame represents 0.1 seconds (time starts at t=0).

2. **Kinetic Model (ODE)**:
   The reaction follows the ODEs:
   dA/dt = -k1 * A
   dB/dt = k1 * A - k2 * B
   Initial conditions at t=0: A=1.0, B=0.0.
   You must use the standard 4th-order Runge-Kutta (RK4) method with a fixed time step of dt=0.1 seconds to simulate this system.

3. **Log-Likelihood Evaluator**:
   Write a Python script `/home/user/evaluate_ll.py` that takes two float arguments, `k1` and `k2`, from the command line.
   The script must:
   - Read the experimental data from `/home/user/signal.csv`.
   - Run the RK4 ODE solver up to the time of the last frame in the video.
   - Compute the log-likelihood using a Gaussian error model: LL = -0.5 * sum( (A_simulated[i] - A_experimental[i])^2 / sigma^2 ), where sigma = 0.05.
   - Print *only* the final LL value to standard output as a float (e.g., `-42.123456789`).

Ensure your RK4 implementation is precise and your script handles the I/O exactly as specified, as it will be rigorously tested against a reference implementation using various k1 and k2 values.