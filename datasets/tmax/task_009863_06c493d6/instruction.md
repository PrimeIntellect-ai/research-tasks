You are a data analyst optimizing a simple anomaly detection system. We have a historical dataset of machine telemetry at `/home/user/data.csv`. The file has a header and three columns: `temp`, `vibration`, and `failure` (where `failure` is 1 if the machine failed, 0 otherwise).

Your task is to build a fast, pure Bash/CLI (e.g., `awk`, `bc`) Naive Bayes inference pipeline that predicts the probability of failure for new incoming data, and then benchmark its performance.

Step 1: Feature Engineering & Bayesian Inference
For a new observation with `temp=75` and `vibration=42`:
1. First, compute discretized features using integer division by 10 (e.g., `temp_bin = int(temp/10)`, `vib_bin = int(vibration/10)`). For the new observation, `temp_bin=7` and `vib_bin=4`.
2. Using the entire dataset in `/home/user/data.csv`, calculate the exact counts to determine:
   - The prior probabilities $P(failure=1)$ and $P(failure=0)$.
   - The conditional probabilities $P(temp\_bin=7 | failure=1)$ and $P(temp\_bin=7 | failure=0)$.
   - The conditional probabilities $P(vib\_bin=4 | failure=1)$ and $P(vib\_bin=4 | failure=0)$.
3. Using the Naive Bayes assumption (that features are conditionally independent given the failure class), calculate the posterior probability that the machine will fail ($failure=1$):
   $P(failure=1 | temp\_bin=7, vib\_bin=4)$
4. Round the final normalized probability to exactly 4 decimal places and save it in `/home/user/posterior.txt`.

Step 2: Inference Benchmarking
1. Write a shell command (or script) that computes this specific posterior probability calculation 1000 times in a row in a loop (you do not need to re-read the CSV each time if you extract the probabilities first, but the calculation itself must happen 1000 times).
2. Measure the wall-clock execution time of this 1000-iteration loop.
3. Extract ONLY the total real execution time (in seconds, as a numeric value) and save it to `/home/user/benchmark.txt`.

Constraints:
- You must use standard shell tools (Bash, awk, bc, grep, etc.). Do not use Python, R, or other programming languages.