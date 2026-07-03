A researcher in our lab lost the source code for their anomalous diffusion simulator, but they managed to salvage a video recording of one of the 1D particle tracks (`/app/particle.mp4`) and some notes on the mathematical model. 

We need you to recreate the Monte Carlo simulation program exactly, so we can reproduce their results.

**Step 1: Video Analysis & Density Estimation**
The video `/app/particle.mp4` shows a white particle (2x2 pixels) moving horizontally on a black 64x64 pixel background.
1. Extract the X-coordinate of the particle in each frame. The X-coordinate is defined as the mean X-index (column index) of all pixels where the grayscale intensity is strictly greater than 128.
2. Calculate the frame-to-frame step sizes: $dx_t = x_t - x_{t-1}$.
3. Fit a normal distribution to these step sizes to find the sample variance of the steps. Calculate the sample variance as $s^2 = \frac{1}{N-1} \sum (dx_i - \overline{dx})^2$. 
4. Round this variance to the nearest integer. This integer is $K$, the number of microscopic collisions per macroscopic observation step.

**Step 2: Monte Carlo Simulator**
Create a Python script at `/home/user/mc_sim.py` that takes exactly two integer command-line arguments: a `seed` and `num_steps`. 
The script must simulate the random walk for `num_steps` macroscopic steps and print ONLY the final integer position to standard output.

*The Model Rules:*
- The particle starts at position `0`.
- The simulation uses a Linear Congruential Generator (LCG) for randomness. The state is initialized to `seed`. 
- The LCG update rule is: $state_{n+1} = (1103515245 \times state_n + 12345) \pmod{2^{31}}$
- For each of the `num_steps` macroscopic steps, the particle undergoes exactly $K$ microscopic collisions.
- For each microscopic collision:
  1. Advance the LCG state to get the next pseudo-random integer $V$.
  2. The microscopic step displacement is $(V \pmod 3) - 1$. (This evaluates to -1, 0, or 1).
  3. Add this microscopic displacement to the particle's total position.

Ensure your script is efficient and bit-exact. We will verify your script against an oracle using thousands of random `seed` and `num_steps` pairs.