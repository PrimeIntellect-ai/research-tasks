You are a data scientist analyzing the acoustic signature of a dual-mass vibration system (coupled damped oscillators) for predictive maintenance. We have a recording of the system's vibrations after an impulse excitation, located at `/app/vibration_data.wav`. 

The system is governed by the following system of ODEs:
m1 * x1''(t) + c1 * x1'(t) + (k1 + k2) * x1(t) - k2 * x2(t) = 0
m2 * x2''(t) + c2 * x2'(t) + (k2 + k3) * x2(t) - k2 * x1(t) = 0

We know:
- m1 = 1.0 kg
- m2 = 1.5 kg
- Initial conditions: x1(0) = 1.0, x2(0) = 0.0, x1'(0) = 0.0, x2'(0) = 0.0.
- The audio recording in `/app/vibration_data.wav` represents the displacement of the first mass, `x1(t)`, sampled at 1000 Hz for 10 seconds.

Your task:
1. Load and process the audio signal using spectral analysis (e.g., FFT) to obtain initial estimates for the system's eigenfrequencies and damping ratios.
2. Use numerical ODE solving (e.g., `scipy.integrate.solve_ivp`) combined with an optimization routine to fit the model to the observed `x1(t)` data to extract the unknown parameters: `c1`, `c2`, `k1`, `k2`, `k3`.
3. Beware: Due to the high correlation between the coupling stiffness `k2` and the individual stiffnesses, the Jacobian during standard nonlinear least-squares fitting (e.g., Levenberg-Marquardt) will likely become near-singular. You will need to implement a robust fitting strategy (such as Tikhonov regularization, bounds, or alternative optimization methods) to achieve convergence.
4. Perform convergence testing to ensure your ODE solver tolerances are strict enough to not bias the optimization.
5. Save the best-fit parameters in a JSON file at `/home/user/parameters.json` with the following exact keys: `"c1"`, `"c2"`, `"k1"`, `"k2"`, `"k3"`. The values must be floats.

Your Python scripts and any virtual environment should be managed within `/home/user/`.