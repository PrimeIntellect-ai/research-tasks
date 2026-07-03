You are a bioinformatics analyst working on a statistical model for sequence matching scores. 

We are using a Markov Chain Monte Carlo (MCMC) sampler written in Go to estimate the posterior distribution of a mutation rate parameter `mu`. The code is located at `/home/user/mcmc.go` and it reads a dataset from `/home/user/sequences.csv`.

However, we are facing a critical reproducibility issue. The MCMC chain is seeded with a fixed random seed (`rand.Seed(42)`), but every time we run the program, the trace diverges after a few dozen iterations. 

After some debugging, we discovered the issue: the `LogLikelihood` function splits the sequence data into 10 chunks and computes the sum of the log-likelihoods concurrently. Because the goroutines finish in an unpredictable order, the results are sent to the channel and accumulated in a random order. Due to floating-point addition not being strictly associative, this non-deterministic reduction order results in tiny variations at the `1e-13` precision level. These tiny variations eventually cause the Metropolis-Hastings acceptance step to make different decisions, causing the MCMC trajectories to diverge.

Your task is to:
1. Modify `/home/user/mcmc.go` to fix the floating-point reduction order issue. You must ensure that the chunk results are always summed in ascending order of their `ChunkID` (from 0 to 9) before returning the total log-likelihood.
2. Compile and run the fixed MCMC program. It is already configured to run 100 iterations and write the output to `/home/user/trace.csv` (with columns `Iteration,Mu,LogLikelihood`).
3. Ensure the final `trace.csv` file is successfully generated. Our automated test will check the exact contents of `/home/user/trace.csv` to verify that the MCMC chain is now perfectly reproducible and mathematically correct according to the sorted reduction order.

Do not change the random seed, the number of iterations, or the core statistical formulas—only fix the concurrent accumulation logic in the `LogLikelihood` function.