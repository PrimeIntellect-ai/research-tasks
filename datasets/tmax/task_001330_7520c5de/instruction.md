You are acting as an automated research assistant for a computational biophysics lab. We are analyzing a time-series video from a novel spectroscopic assay of a single molecule, which transitions between a "Dark" state and a "Bright" state.

You have been provided with the raw experimental video: `/app/spectroscopy_feed.mp4`. The video has a resolution of 64x64 pixels.

Your goal is to extract the fluorescence signal, build a 2-state graph model, and use a Monte Carlo method to estimate the transition probabilities between the states, comparing it against a null hypothesis.

Step 1: Signal Extraction
Using standard CLI tools (like `ffmpeg`, `awk`, or custom bash/C++), extract the mean luminance (grayscale value) of the central 16x16 pixel region (x from 24 to 39, y from 24 to 39, 0-indexed) for every frame in the video. This will give you a 1D time-series array of intensities.

Step 2: Monte Carlo Markov Chain (MCMC) Parameter Estimation in C++
Write a C++ program (to be compiled with `g++ -O3 -std=c++17`) that reads your extracted 1D signal.
Model the sequence of true states $S_t \in \{0, 1\}$ (where 0 is Dark and 1 is Bright) as a Markov chain with unknown transition probabilities $p_{01} = P(S_{t+1}=1 | S_t=0)$ and $p_{10} = P(S_{t+1}=0 | S_t=1)$.
Assume the observed mean luminance $Y_t$ at time $t$ is normally distributed given $S_t$:
- If $S_t = 0$, $Y_t \sim \mathcal{N}(\mu_0=50, \sigma=10)$
- If $S_t = 1$, $Y_t \sim \mathcal{N}(\mu_1=200, \sigma=10)$

Using a Monte Carlo method (e.g., Metropolis-Hastings or Gibbs sampling), estimate the most likely parameters for $p_{01}$ and $p_{10}$ given the observed sequence $Y_t$. 

Step 3: Statistical Hypothesis Output
Calculate the log-likelihood of your estimated MAP (Maximum A Posteriori) Markov model vs. a Null Hypothesis model (where $p_{01}=0.5$ and $p_{10}=0.5$, i.e., completely independent random states).

Your C++ program should output a single text file to `/home/user/results.csv` with exactly three lines in the following format:
```
P01,<your_estimated_p01>
P10,<your_estimated_p10>
LLR,<log_likelihood_ratio_of_MAP_vs_Null>
```

Work completely in the terminal. You may install standard C++ libraries or tools via `apt` if needed, but the core estimation logic must be your own C++ code. Make sure to compile and run your code to generate the final `results.csv` file.