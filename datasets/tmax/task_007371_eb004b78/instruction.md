You are a bioinformatics analyst working on primer binding kinetics. You need to estimate the decay of primer concentration over time using an ODE, but the decay rate depends on the upper bound of the confidence interval of sequence alignment scores. 

You must build a reproducible pure-Bash/Awk pipeline to accomplish this. You may not use Python, R, or C++. Use only standard Linux utilities (bash, awk, coreutils, etc.).

**Part 1: Bootstrap Confidence Interval**
You are given a dataset of 10 primer alignment scores in `/home/user/alignments.txt`.
To make the bootstrap fully reproducible without relying on specific random number generator implementations, you are provided with `/home/user/random_indices.txt`. This file contains 10,000 random integers (between 1 and 10), one per line.
1. Perform 1000 bootstrap resamples of the alignment scores. Each resample consists of 10 draws.
2. Use the indices from `/home/user/random_indices.txt` strictly in order. The first 10 indices correspond to the 10 draws for the first resample, the next 10 for the second resample, and so on.
3. Calculate the mean score for each of the 1000 resamples.
4. Sort the 1000 means in ascending order.
5. Find the 95% confidence interval bounds by taking the 25th value (lower bound) and the 975th value (upper bound) in the sorted means array.

**Part 2: ODE Numerical Solving**
The primer concentration $C(t)$ degrades according to the following ordinary differential equation:
$dC/dt = - k \times C$
where the decay constant $k$ is calculated as `Upper_Bound / 100` (using the upper bound from Part 1).

1. Implement a simple Forward Euler numerical solver in `awk` or `bash` to simulate this ODE.
2. Initial conditions: $C(0) = 100.0$.
3. Time step: $dt = 0.1$.
4. Number of steps: 50 (so you will compute $C$ at $t = 0.1, 0.2, ..., 5.0$).
5. At each step, update $C_{new} = C_{old} + (dC/dt) \times dt$.

**Output**
Calculate the final concentration at step 50. Save this single numeric value, rounded to exactly 4 decimal places, in `/home/user/final_concentration.txt`.