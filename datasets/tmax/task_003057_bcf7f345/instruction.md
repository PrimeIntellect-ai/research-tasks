You are an MLOps engineer tracking the accuracy of model experiment artifacts in a highly constrained environment. You have a metadata file containing extracted features, model weights, and actual target values for several inference runs.

Your task is to build a minimal ETL and analysis pipeline in **C** that reads this data, calculates the model's accuracy, and performs a Bayesian update on the model's success probability.

**Data Location:** `/home/user/experiments.csv`
**Input Format:** `exp_id,f1,f2,f3,w1,w2,w3,target,prior_alpha,prior_beta`
- `exp_id`: A single character representing the experiment (e.g., 'A', 'B')
- `f1, f2, f3`: Floating point feature values
- `w1, w2, w3`: Floating point weight values
- `target`: The expected floating point output
- `prior_alpha, prior_beta`: Integer parameters for the Beta distribution prior of the model's success rate. (These are identical for all rows of the same `exp_id`).

**Processing Requirements:**
1. **Linear Algebra & Numerical Accuracy:** For each row, compute the predicted value as the dot product of the features and weights: `prediction = (f1*w1) + (f2*w2) + (f3*w3)`.
2. A prediction is considered a "success" if the absolute difference between the `prediction` and the `target` is strictly less than `0.1`. Otherwise, it is a "failure".
3. **Bayesian Inference:** Treat the successes and failures as binomial trials. For each `exp_id`, use the provided `prior_alpha` and `prior_beta` to compute the posterior Beta distribution parameters:
   - `posterior_alpha = prior_alpha + total_successes`
   - `posterior_beta = prior_beta + total_failures`
4. Calculate the expected value of the posterior distribution for each `exp_id`: `expected_value = posterior_alpha / (posterior_alpha + posterior_beta)`.

**Deliverables:**
Write a C program (e.g., `/home/user/analyze.c`), compile it, and execute it so that it reads `/home/user/experiments.csv` and generates an output report at `/home/user/results.csv`.

**Output Format for `/home/user/results.csv`:**
```
exp_id,posterior_alpha,posterior_beta,expected_value
```
- Print one row per unique `exp_id` in alphabetical order.
- Format the `expected_value` to exactly 4 decimal places (e.g., `0.6000`).

Ensure your C code handles the file operations and floating-point logic safely. Do not use Python, R, or other scripting languages for the core logic—you must use C.