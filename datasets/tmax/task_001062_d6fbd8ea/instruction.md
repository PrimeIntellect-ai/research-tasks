You are an AI assistant helping a physics researcher analyze an experimental video of a damped harmonic oscillator. The experiment recorded a bright, moving point mass (a pendulum bob) over time.

You must perform the following complete workflow:

1. **Environment Setup**: Set up your Python scientific environment. You may need to install libraries like `opencv-python`, `emcee`, `scipy`, and `numpy`.
2. **Video Processing**: A video of the experiment is located at `/app/experiment.mp4`. The video is 640x480 at 30 frames per second. Extract the $x$-coordinate of the object in each frame. The object is visually distinct as the brightest spot (white/light gray) against a dark background.
3. **MCMC Parameter Estimation**: 
   Model the trajectory using the damped harmonic oscillator equation:
   $$x(t) = A e^{-\gamma t} \cos(\omega t + \phi) + x_0$$
   where $t$ is time in seconds (frame index / 30).
   Write a Python script that uses Markov Chain Monte Carlo (MCMC) to estimate the posterior distributions of the parameters: Amplitude ($A$), damping coefficient ($\gamma$), angular frequency ($\omega$), phase shift ($\phi$), and baseline position ($x_0$).
   Use uninformative (uniform) priors over reasonable physical bounds. Extract the mean of the posterior samples as your point estimates for $\gamma$ and $\omega$.
4. **Bootstrap Confidence Intervals**:
   Compute the residual errors $r_i = x_{obs, i} - x_{model, i}$ using your point estimates.
   Perform a bootstrap resampling of these residuals (1000 iterations) to estimate the 95% confidence interval for the measurement noise variance (the variance of the residuals).
5. **Output**:
   Save your final estimates to a JSON file at `/home/user/results.json` with exactly the following keys:
   - `"gamma"`: (float) the posterior mean of the damping coefficient
   - `"omega"`: (float) the posterior mean of the angular frequency
   - `"noise_variance_ci_lower"`: (float) the lower bound of the 95% CI of the noise variance
   - `"noise_variance_ci_upper"`: (float) the upper bound of the 95% CI of the noise variance

Your code must be entirely contained in `/home/user/analysis.py` and produce the `/home/user/results.json` file when run.

Good luck!