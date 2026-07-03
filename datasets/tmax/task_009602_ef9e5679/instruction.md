You are helping a data scientist debug a C++ Markov Chain Monte Carlo (MCMC) sampler. 

The sampler is located at `/home/user/sampler.cpp`. It estimates the posterior mean of a Gaussian distribution given a large dataset (`/home/user/dataset.txt`). The script currently compiles and runs, outputting a sequence of sampled means to `chain.csv`.

However, the results are slightly inaccurate and diverge from our highly precise reference implementation. Due to the large size of the dataset and the specific ordering of the values, the naive summation used in the `log_likelihood` function suffers from floating-point accumulation errors. This tiny difference in the calculated log-likelihood eventually causes the MCMC chain to make different acceptance decisions and diverge completely from the true path.

Your task:
1. Examine `/home/user/sampler.cpp`.
2. Modify the `log_likelihood` function to use **Kahan summation** instead of naive summation. This will preserve floating-point precision when accumulating the log-probabilities across the large dataset.
3. Compile the sampler from source using `g++ -O3 std=c++11 sampler.cpp -o sampler`.
4. Run the sampler. It will generate a file named `chain.csv` in the current directory.
5. Compare your `chain.csv` to the provided `/home/user/reference_chain.csv`. They must match exactly line-by-line.
6. Once they match, copy your correctly generated `chain.csv` to `/home/user/final_chain.csv`.

Do not change the random seed, the proposal distribution, or the number of iterations in the sampler. Only fix the summation algorithm in the `log_likelihood` function.