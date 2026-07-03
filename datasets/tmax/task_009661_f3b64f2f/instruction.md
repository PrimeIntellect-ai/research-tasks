You are a Machine Learning Engineer preparing a robust training dataset from multiple noisy sensors. You must fuse the sensor data using Bayesian inference to estimate the true underlying signal, and then assess the quality of this new feature by examining its correlation with the target variable using bootstrap methods. 

Because our data engineering pipeline relies on Python and our statistical modeling pipeline relies on R, you must use both languages to complete this task.

**Data Available:**
In `/home/user/data/`, there are four CSV files:
- `sensor_a.csv`: Columns `timestamp` and `value_a` (Sensor A measurements)
- `sensor_b.csv`: Columns `timestamp` and `value_b` (Sensor B measurements)
- `sensor_c.csv`: Columns `timestamp` and `value_c` (Sensor C measurements)
- `target.csv`: Columns `timestamp` and `target` (The outcome variable we want to predict)

These sensors frequently drop packets, so they do not have identically matching rows.

**Phase 1: Multi-source Data Joining (Python)**
Write a Python script at `/home/user/join_data.py` that reads the four CSV files and performs an **inner join** on the `timestamp` column across all four datasets. 
Save the resulting merged dataset to `/home/user/data/joined.csv`.

**Phase 2: Bayesian Inference & Bootstrap Correlation (R)**
Write an R script at `/home/user/analyze.R` that reads `/home/user/data/joined.csv` and performs the following statistical modeling:

1. **Bayesian Signal Estimation**: 
   Assume the true signal at any timestamp $t$, denoted as $\mu_t$, has a Normal prior distribution: $\mu_t \sim \mathcal{N}(\text{mean}=0, \text{variance}=100)$.
   The three sensors provide independent measurements of $\mu_t$ with known noise variances:
   - Sensor A variance: $\sigma_A^2 = 2.0$
   - Sensor B variance: $\sigma_B^2 = 4.0$
   - Sensor C variance: $\sigma_C^2 = 1.0$
   
   Calculate the posterior mean of the signal $\mu_{post, t}$ for each row using the standard precision-weighted conjugate update for Normal distributions. 

2. **Correlation & Bootstrap**:
   - Compute the Pearson correlation coefficient between the calculated posterior mean ($\mu_{post}$) and the `target` column.
   - Use empirical bootstrap resampling to estimate the 95% Confidence Interval for this correlation. 
   - **Bootstrap specifications:** Use $B=10,000$ iterations. Sample pairs of $(\mu_{post}, \text{target})$ with replacement. Set the random seed to `42` right before the bootstrap loop (`set.seed(42)`). Calculate the 2.5th and 97.5th percentiles of the bootstrapped correlations.

**Phase 3: Reporting**
Your R script must output a JSON file at `/home/user/results.json` containing exactly these keys:
- `"joined_rows"`: (integer) The number of rows in the joined dataset.
- `"correlation"`: (float) The Pearson correlation between the posterior mean and the target.
- `"ci_lower"`: (float) The 2.5th percentile of the bootstrapped correlation.
- `"ci_upper"`: (float) The 97.5th percentile of the bootstrapped correlation.

Round all float values to 4 decimal places.

Run your scripts and ensure the `results.json` is successfully created. You may install any necessary packages (e.g., `pandas` in Python, `jsonlite` in R).