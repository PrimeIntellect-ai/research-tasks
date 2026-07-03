You are a bioinformatics analyst working on modeling nucleotide sequence evolution. We use a Continuous-Time Markov Chain (CTMC) to model mutation rates. 

We have a C++ program, `/home/user/simulator.cpp`, which does the following:
1. Reads a 4x4 substitution rate matrix $Q$ from an HDF5 file `/home/user/q_matrix.h5` (dataset name: `Q`).
2. Calculates the theoretical stationary distribution $\pi$ by finding the null space of $Q^T$ using SVD decomposition (via the Eigen3 library).
3. Simulates the evolution of a sequence over time $T=10$ using a Monte Carlo approach, where the probability distribution is iteratively updated using an Euler integration step: $p(t + \Delta t) = p(t) + p(t) Q \Delta t$.
4. Computes the Kullback-Leibler (KL) divergence between the theoretical stationary distribution $\pi$ and the empirical distribution from the Monte Carlo simulation.

**The Problem:**
The numerical integrator in the Monte Carlo simulation diverges and produces `NaN`s because the fixed step-size adaptation is wrong (the time step $\Delta t$ is too large for the rate matrix, leading to negative probabilities). 

**Your Task:**
1. Fix the step-size logic in `/home/user/simulator.cpp`. The step size `dt` must be adaptively set such that $dt < 1.0 / \max_i(|Q_{ii}|)$ to guarantee stable integration. 
2. Compile the code. (Assume Eigen3 is at `/usr/include/eigen3` and link against HDF5: `g++ -O3 simulator.cpp -o simulator -I/usr/include/eigen3 -lhdf5_cpp -lhdf5`).
3. Run the program. It should write the final results to `/home/user/results.txt` with exactly the following format (values rounded to 4 decimal places):
```
Theoretical: [v1, v2, v3, v4]
Empirical: [v1, v2, v3, v4]
KL_Divergence: [value]
```

Fix the code, compile it, and generate the `results.txt` file.