You are a bioinformatics analyst working with raw nanopore sequencing signal data (often called "squiggles"). The raw electrical current data is very noisy and needs to be smoothed before basecalling can begin. You must write a Bash script to process this signal, test for convergence of an iterative smoothing filter, and evaluate the numerical stability (energy) of the signal.

Your task is to create a Bash script at `/home/user/analyze_squiggles.sh` that performs the following operations:

1. **Input Data**: The raw signal is provided in `/home/user/raw_signal.tsv`. It contains a single column of floating-point numbers representing the current at time `t`. Let's denote this array as `S` with length `N`. Indices are `0` to `N-1`.

2. **Iterative Smoothing**: Apply a 3-point moving average filter iteratively. 
   For each iteration `k`, calculate the new signal `S_new` based on the old signal `S_old`:
   - For boundary points: `S_new[0] = S_old[0]` and `S_new[N-1] = S_old[N-1]`
   - For all interior points (`0 < i < N-1`): 
     `S_new[i] = 0.5 * S_old[i] + 0.25 * S_old[i-1] + 0.25 * S_old[i+1]`

3. **Convergence Testing**: After each iteration, calculate the maximum absolute change across all points: `max_change = max(|S_new[i] - S_old[i]|)`.
   - The smoothing process has converged when `max_change < 0.001`.
   - Once converged, stop iterating. Do not perform any further smoothing iterations.
   - Write the total number of completed iterations to `/home/user/iterations.txt`.

4. **Numerical Stability (Energy Tracking)**: To ensure the signal isn't diverging, calculate the total "Energy" of the converged signal. Energy is defined as the sum of the squares of all signal values: `Energy = sum(S[i]^2)`.
   - Write the final Energy value, rounded to exactly 4 decimal places, to `/home/user/final_energy.txt`.

5. **Output**: Save the final smoothed signal to `/home/user/smoothed.tsv` (one value per line, printed to 6 decimal places).

Requirements:
- You must implement the logic primarily using Bash (tools like `awk`, `bc`, `sed` are standard and encouraged). 
- Ensure your script is executable (`chmod +x`).
- Execute your script to generate the required output files:
  - `/home/user/iterations.txt`
  - `/home/user/final_energy.txt`
  - `/home/user/smoothed.tsv`