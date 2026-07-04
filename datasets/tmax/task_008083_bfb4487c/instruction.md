You are an MLOps engineer responsible for managing an experiment tracking pipeline. We are testing a new Bayesian inference module written in C, which analyzes experiment logs to estimate success probabilities using a Beta-Binomial model.

Your task is to fix the provided C program, run it on our dataset, and correctly package the resulting model artifacts for our large-scale storage system.

**Environment Setup:**
- You have a dataset at `/home/user/experiment_data.txt`. Each line contains an experiment ID followed by a space-separated sequence of tokens representing outcomes (`S` for Success, `F` for Failure). 
  Example: `EXP_01 S F S S`
- You have a provided (but buggy) C source file at `/home/user/src/analyze.c`. 
- The target output directory for artifacts is `/home/user/artifacts/`.

**Objectives:**
1. **Fix the C Code:** The program `/home/user/src/analyze.c` is supposed to:
   - Read `/home/user/experiment_data.txt`.
   - Tokenize each line to extract the experiment ID and the sequence of `S` and `F` tokens.
   - Calculate the Bayesian posterior expected value of the success probability using a Uniform prior, which is equivalent to a Beta(1, 1) prior. 
     *Formula: Posterior Mean = (Count_S + 1) / (Count_S + Count_F + 2)*
   - Write the results to `/home/user/artifacts/results.csv` in the format `EXP_ID,POSTERIOR_MEAN` formatted to exactly 4 decimal places (e.g., `EXP_01,0.6000`).
   *Note: The provided C code has bugs related to tokenization and mathematical calculation (specifically integer division). Find and fix them.*

2. **Compile and Run:** 
   - Install any necessary build tools (like `gcc`) if they aren't present.
   - Compile the fixed C program to `/home/user/src/analyze`.
   - Run the executable to generate the `results.csv` file in the artifacts directory.

3. **Artifact Management:** 
   - Once `results.csv` is successfully generated, package the entire `/home/user/artifacts/` directory into a gzip-compressed tarball at `/home/user/artifacts.tar.gz`. 
   - Ensure the tarball contains the `artifacts` directory at its root (i.e., extracting it should create an `artifacts/` folder).

Ensure all final files are exactly at the specified paths.