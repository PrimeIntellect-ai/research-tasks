You are a data scientist attempting to reproduce an older population dynamics model fitting pipeline. The original developer left behind an image of their handwritten notes containing the specific parameters and initial conditions for the model, as well as a compiled reference binary (oracle) of the integration engine.

Your task is to write a Python-based numeric integrator that perfectly replicates the behavior of the oracle binary. 

Step 1: Inspect the handwritten notes
Extract the parameters from `/app/model_params.png`. You can use `tesseract` to read the text. The image contains the parameters (alpha, beta, delta, gamma) and the initial conditions (x0, y0) for a standard Lotka-Volterra predator-prey model:
dx/dt = alpha*x - beta*x*y
dy/dt = delta*x*y - gamma*y

Step 2: Implement the Integrator
Create a Python script at `/home/user/integrate_model.py`.
The script must take exactly two positional CLI arguments:
1. `t_end`: A float representing the final time (start time is always t=0).
2. `num_steps`: An integer representing the exact number of integration steps to take.

Your script must perform numerical integration from t=0 to t=`t_end` using the standard 4th-order Runge-Kutta (RK4) method, with a fixed step size of `dt = t_end / num_steps`. Use the parameters and initial conditions extracted from the image. 

Step 3: Output Format
The script must print exactly one line to standard output containing the final values of `x` and `y` at `t_end`, separated by a single space, and rounded to exactly 4 decimal places (e.g., `45.1234 18.5678`).

Step 4: Regression Testing
Ensure your script matches the output of the provided reference binary `/app/oracle_integrator` for various combinations of `t_end` and `num_steps`. An automated regression suite will test your script against the oracle using thousands of random inputs.