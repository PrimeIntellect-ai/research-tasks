You are a data analyst working on an A/B testing pipeline. You need to write a C++ program to process a batch of experiment results and update your Bayesian priors, as well as a bash script to orchestrate the pipeline.

I have placed a dataset at `/home/user/experiment_data.csv`. 
The file contains raw, noisy data from a recent test. 

Your task is to:
1. Write a C++ program named `/home/user/bayesian_updater.cpp` that reads the CSV file and computes the posterior parameters of a Beta-Binomial model for each valid experimental variant.
2. The program must accept two command-line arguments in this exact order: `alpha_prior` (integer) and `beta_prior` (integer).
3. The program must strictly enforce the following data schema on each row. Any row (including the header) that violates *any* of these rules must be completely ignored:
   - Must have exactly 3 comma-separated columns.
   - Column 1 (`uid`): Must be a valid non-negative integer.
   - Column 2 (`variant`): Must be exactly the string "A" or "B".
   - Column 3 (`converted`): Must be exactly the integer 0 or 1.
4. For each valid variant, compute the Beta posterior parameters:
   - `alpha_post = alpha_prior + successes` (where converted = 1)
   - `beta_post = beta_prior + failures` (where converted = 0)
5. The C++ program must output the results to `/home/user/posteriors.csv` with the exact header `variant,alpha_post,beta_post`. The rows must be sorted alphabetically by variant (A, then B).
6. Create an executable bash script at `/home/user/run_pipeline.sh` that compiles your C++ program using `g++` (with `-std=c++17`) and runs it on the dataset with `alpha_prior=2` and `beta_prior=5`.

Ensure your scripts are fully automated and execute cleanly without further user input.