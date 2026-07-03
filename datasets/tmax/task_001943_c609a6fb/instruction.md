You are a statistical researcher estimating the volume of high-dimensional hyperspheres using Monte Carlo numerical integration. You need to implement the simulation and convergence testing using purely Bash and standard Linux CLI tools (like `awk`, `bc`, etc.).

Step 1: Write a Bash script `/home/user/mc_volume.sh` that calculates the estimated volume.
- It must accept exactly 4 arguments: `D` (dimensions), `R` (radius), `N` (total random points to sample), and `P` (number of parallel processes).
- It should divide the `N` points equally among `P` parallel processes (you can assume `N` is always divisible by `P`).
- Run the `P` processes in parallel using shell background jobs (`&` and `wait`) or `xargs -P`.
- Inside the parallel jobs, use `awk` to generate random points. For each point, generate `D` coordinates, each uniformly distributed in the range `[-R, R]`. A point is inside the hypersphere if the sum of the squares of its coordinates is less than or equal to `R^2`.
- Make sure each parallel `awk` process is initialized with a different random seed (e.g., using `$RANDOM` or `NR` mixed with time).
- Sum the 'inside' counts from all `P` processes.
- Calculate the final estimated volume: `Volume = (2*R)^D * (total_inside / N)`.
- The script must print *only* the final estimated volume to standard output as a decimal number.

Step 2: Write a Bash script `/home/user/convergence.sh` to perform a convergence test.
- The test targets a 3-dimensional hypersphere with a radius of 2.0.
- Start with `N = 1000` and `P = 4`.
- Run `mc_volume.sh` to get the estimated volume.
- In a loop, keep doubling `N` (2000, 4000, 8000, ...) and run the simulation again.
- Stop the loop when the absolute difference between the current estimated volume and the immediately previous estimated volume is strictly less than `0.2`.
- Once the stopping condition is met, write the final `N` and its corresponding estimated volume to `/home/user/convergence_result.txt` in exactly this format:
  `N: <N>, Volume: <Vol>`
  (e.g., `N: 16000, Volume: 33.456`)

Ensure your scripts have executable permissions. 
Do not use Python, Perl, or any non-standard Bash utilities.