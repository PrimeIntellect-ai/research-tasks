You are acting as a data scientist in a performance-critical environment. You have been handed a raw dataset of model embeddings (`/home/user/embeddings.csv`) and a reference embedding (`/home/user/reference.csv`). 

Your task is to write a highly efficient C program that cleans this dataset, validates the model's outputs using linear algebra, computes statistical confidence intervals, and benchmarks the inference computation time.

Here are the requirements:

1. **Data Schema Enforcement**: 
   The file `/home/user/embeddings.csv` contains thousands of lines. A valid line consists of exactly 100 comma-separated floating-point numbers. Some lines are corrupted (they contain non-numeric characters, or have fewer/more than 100 dimensions). Your program must parse the CSV and strictly discard any invalid lines.

2. **Linear Algebra & Model Validation**:
   The file `/home/user/reference.csv` contains exactly one valid line with 100 comma-separated floats. 
   For every *valid* line in the embeddings dataset, calculate the dot product between that embedding and the reference embedding. 
   The model is considered to have produced "VALID" outputs overall if the sample mean of these dot products is strictly greater than 25.0. Otherwise, it is "INVALID".

3. **Hypothesis Testing & Confidence Intervals**:
   Calculate the sample mean and the sample standard deviation of the dot products. 
   Compute the 95% Confidence Interval for the mean using the standard normal approximation (Z = 1.96). 

4. **Inference Benchmarking**:
   You must measure the time it takes to compute *just* the dot products and statistics. Start your timer after all file reading and schema enforcement is done (e.g., have the valid vectors loaded in memory), and stop it immediately after computing the mean, standard deviation, and CI bounds. Use `clock_gettime(CLOCK_MONOTONIC, ...)` for high-resolution benchmarking.

5. **Output Requirements**:
   Write your C program to `/home/user/validate_model.c` and compile it to `/home/user/validate_model` using `gcc -O3 -lm`.
   When executed, your program must write an output log file to `/home/user/results.log` with exactly the following format (replace brackets with actual values, floats rounded to exactly 4 decimal places):

   ```
   Valid Rows: [integer]
   Mean Dot Product: [float.4f]
   95% CI Lower: [float.4f]
   95% CI Upper: [float.4f]
   Status: [VALID or INVALID]
   Compute Time: [float.6f] seconds
   ```

Do not use any external libraries other than the C Standard Library and `math.h`.