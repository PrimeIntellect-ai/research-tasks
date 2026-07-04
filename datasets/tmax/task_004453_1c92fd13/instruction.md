I am a researcher running MCMC simulations. I have been using an old compiled utility to calculate the Gelman-Rubin convergence diagnostic ($\hat{R}$) for my MCMC chains, but the original source code was lost. The utility is located at `/app/gelman_rubin_oracle` and is a stripped binary.

The utility is called via the command line with the following arguments:
`./gelman_rubin_oracle <M> <N> <val_1_1> <val_1_2> ... <val_1_N> <val_2_1> ... <val_M_N>`
where:
- `<M>` is the number of chains (integer $\ge 2$)
- `<N>` is the number of samples per chain (integer $\ge 2$)
- The remaining arguments are the $M \times N$ sample values as floating-point numbers. The samples are provided chain by chain (i.e., all $N$ samples of the first chain, then all $N$ samples of the second chain, etc.).

The utility outputs a single floating-point number, formatted to exactly 6 decimal places (e.g., `1.042310`), representing the $\hat{R}$ statistic. 

Your task is to reverse-engineer the exact mathematical formula used by this oracle and write a C++ program that perfectly replicates its behavior. 
1. Write your C++ source code to `/home/user/gelman_rubin.cpp`.
2. Compile it to an executable at `/home/user/gelman_rubin` (e.g., `g++ -O3 /home/user/gelman_rubin.cpp -o /home/user/gelman_rubin`).

Your compiled executable must produce bit-exact equivalent standard output to the oracle for any valid inputs. I will test your executable against the oracle using thousands of random MCMC chain samples.