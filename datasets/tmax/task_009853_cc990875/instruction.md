You are a data engineer building a validation step for an ETL pipeline that pre-computes Bayesian probabilities for a downstream fraud detection system. 

Your task is to write a C++ program that reads an input dataset, enforces data schema rules, performs Bayesian inference, tests numerical accuracy against expected values, and benchmarks the inference step.

Write a C++ source file at `/home/user/etl_validator.cpp` and compile it to an executable at `/home/user/etl_validator`.

**Input Data:**
The file `/home/user/input_data.csv` contains comma-separated values with a header:
`id,prior_prob,likelihood,evidence,expected_posterior`

**Requirements for the C++ program:**
1. **Data Schema Enforcement:**
   Read the CSV. For each row (skipping the header):
   - `id` must be parsed as an integer.
   - `prior_prob`, `likelihood`, `evidence`, and `expected_posterior` must be parsed as double-precision floating-point numbers.
   - Schema validation fails if `prior_prob` is < 0.0 or > 1.0, or if `evidence` is exactly 0.0. 
   - If a row fails schema validation, append the exact string `SCHEMA_ERROR: id <id>` to `/home/user/etl_log.txt` and skip further processing for this row.

2. **Bayesian Inference & Numerical Accuracy Testing:**
   For valid rows, calculate the posterior probability using Bayes' theorem:
   `posterior = (likelihood * prior_prob) / evidence`
   
   Test if the calculated `posterior` matches the `expected_posterior`.
   If the absolute difference between `posterior` and `expected_posterior` is strictly greater than `0.0001`, it is considered an accuracy error.
   If an accuracy error occurs, append the string `ACCURACY_ERROR: id <id>` to `/home/user/etl_log.txt`.

3. **Inference Performance Benchmarking:**
   Measure the total wall-clock time spent processing all valid rows (the Bayesian inference and accuracy testing steps, excluding file I/O). 
   After processing all rows, append the string `BENCHMARK_PROCESSED: <count> valid rows` to `/home/user/etl_log.txt` (where `<count>` is the number of rows that passed schema validation).

**Execution:**
Compile your code using `g++ -O3 -o /home/user/etl_validator /home/user/etl_validator.cpp` and then run `/home/user/etl_validator`. 
Ensure `/home/user/etl_log.txt` is created with the exact log strings requested, each on a new line.