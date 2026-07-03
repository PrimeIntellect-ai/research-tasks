You are an MLOps engineer maintaining a custom experiment tracking system. Artifact metrics from multiple test runners are logged locally, but they often contain missing data and need to be joined and evaluated for experiment success probabilities.

Your task is to write a C++ program that combines multiple data streams, cleans the data, calculates simple dimensionality reduction proxies (total variance), and applies Bayesian inference to determine the most promising experiment.

**Requirements:**

1. **Multi-source joining**: Two CSV files will be available at `/home/user/source_a.csv` and `/home/user/source_b.csv`.
   - `source_a.csv` contains: `ExperimentID,Metric1,Metric2`
   - `source_b.csv` contains: `ExperimentID,Metric3,PriorProb`
   - Read and perform an inner join on `ExperimentID`.

2. **Missing value handling**: 
   - Some metric values (Metric1, Metric2, Metric3) are recorded as `-999.0` (indicating missing data).
   - Before any calculations, impute these missing values by replacing them with the *mean* of the valid values for that specific column.

3. **Dimensionality Reduction (Variance)**:
   - Calculate the Population Variance for each of the imputed metric columns (Metric1, Metric2, Metric3).
   - Calculate `Total_Variance` as the sum of the variances of these three metrics. This serves as a proxy for the total informational spread (trace of the covariance matrix).

4. **Bayesian Inference**:
   - For each experiment, calculate the posterior probability of success.
   - You are given the prior probability (`PriorProb`) in the dataset.
   - The *Likelihood* of observing the metrics given a "Successful" experiment ($L_{success}$) is `0.8` if the sum of the experiment's imputed metrics (Metric1 + Metric2 + Metric3) is strictly greater than `20.0`, and `0.4` otherwise.
   - The *Likelihood* of observing the metrics given a "Failed" experiment ($L_{fail}$) is `0.3` if the sum is strictly greater than `20.0`, and `0.7` otherwise.
   - Use Bayes' theorem to compute the posterior probability of success for each experiment.

**Action to perform:**
Write a C++ program at `/home/user/tracker.cpp` and compile it. Execute the program so that it writes its final results to `/home/user/summary.txt` in exactly this format:
```
Highest_Posterior_Exp_ID: <ID>
Total_Variance: <Value rounded to 2 decimal places>
```

(Ensure your program is standard C++17 compliant and requires no external libraries to compile using `g++`).