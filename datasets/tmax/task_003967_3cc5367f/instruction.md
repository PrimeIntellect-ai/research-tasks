Hi, I'm a structural biology researcher trying to run some bulk simulations on a dataset of protein structures (PDB format). I'm using an older structural calculation C library called `struccalc` (version 1.0) to align structures and compute spatial probability distribution metrics. 

However, I'm running into two major issues:
1. The library source is provided in `/app/struccalc-1.0`, but it refuses to compile. I think the Makefile is messed up, and there might be a hardcoded tolerance bug in the matrix factorization module (`matrix_solve.c`) that causes it to fail (return NaN or crash) when it encounters near-singular covariance matrices from certain flat molecular structures. I need you to fix the compilation issue and patch the matrix solver so it handles near-singular inputs gracefully (e.g., by adding a small Tikhonov regularization term $\lambda = 10^{-5}$ to the diagonal before factorization).
2. Once the library is fixed and installed (you can install it locally to `/home/user/local`), I need you to write a C program named `filter_pdb.c` (compiled to `/home/user/filter_pdb`) that uses this library. 

The `filter_pdb` program must act as a filter for my simulation pipeline. It should take a directory path as a command-line argument, read all `.pdb` files in that directory, and determine if each structure is "stable" or "unstable" based on the distribution of its atomic coordinates. 
Specifically, use the `struccalc` library function `compute_wasserstein_dist(PDB* struct1, PDB* ref_struct)` to compare each file against a reference structure located at `/app/reference/ideal.pdb`. 
If the calculated Wasserstein distance is greater than 2.5 Å, or if the structure parsing fails, it should be flagged as UNSTABLE. Otherwise, it is STABLE.

Your program should output exactly one line per `.pdb` file to `stdout` in the following format:
`<filename>: <STABLE|UNSTABLE>`

There are two datasets I want you to test your compiled `/home/user/filter_pdb` against:
- `/app/data/clean/`: Contains stable structures. Your program must classify 100% of these as STABLE.
- `/app/data/evil/`: Contains adversarial/unstable structures (some near-singular, some highly divergent). Your program must classify 100% of these as UNSTABLE.

Please fix the vendored package, write the filtering tool, and ensure it correctly classifies both directories.