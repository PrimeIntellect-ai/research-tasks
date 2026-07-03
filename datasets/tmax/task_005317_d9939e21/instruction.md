You are a performance engineer working on a scientific application that heavily relies on computing information-theoretic distances between probability distributions. Before optimizing the code, you need to establish a baseline, set up parallel execution, and create regression tests.

Your task is to implement and test a numerical integration script for the Kullback-Leibler (KL) Divergence.

Step 1: Implement Numerical Integration
Write a Python script `/home/user/divergence.py` that calculates the KL Divergence $D_{KL}(P || Q)$ using numerical integration via `scipy.integrate.quad`.
- The integration domain should be restricted to $[-20, 20]$.
- $P(x)$ is the probability density function (PDF) of the standard normal distribution $\mathcal{N}(0, 1)$.
- $Q(x)$ is the PDF of a normal distribution $\mathcal{N}(\mu, \sigma^2)$.
- The script must accept two command-line arguments: `--mu` (float) and `--sigma` (float).
- The script must print exactly one line to standard output in the format `mu,sigma,kl_divergence`, where `kl_divergence` is rounded to exactly 4 decimal places.

Step 2: Bash-Based Parallel Execution
Write a bash script `/home/user/run_parallel.sh` that runs `divergence.py` in parallel (e.g., using background jobs `&`, `xargs -P`, or `parallel`) for the following four parameter pairs of (mu, sigma):
- 0.5, 1.5
- 1.0, 1.0
- -0.5, 2.0
- 2.0, 0.8
The bash script must redirect the combined standard output of these runs into a single file at `/home/user/kl_results.log`. (The order of lines in the log file does not matter, as long as all four results are present).

Step 3: Regression Testing
Write a test script `/home/user/test_divergence.py` intended to be run with `pytest`.
- It must import the integration logic from `divergence.py`.
- It must contain a test function that computes the divergence for `mu=1.0` and `sigma=1.0` using your numerical integration function.
- It must assert that the computed value is equal to the analytical expected value of `0.5` with an absolute tolerance of `1e-3`.

Ensure that your scripts are fully functional. You can test your implementation by running `/home/user/run_parallel.sh` and `pytest /home/user/test_divergence.py` in the terminal.