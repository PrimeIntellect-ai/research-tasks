You are a data engineer tasked with building the anomaly detection stage of our ETL pipeline. We process incoming tabular sensor data, but occasionally we receive corrupted or deliberately malformed "adversarial" records that can poison our downstream models.

We have a proprietary, pre-vendored local Python package called `fast_bayes_infer` located at `/app/fast_bayes_infer`. This package contains highly optimized routines for Bayesian inference and multivariate probabilistic modeling. 
However, the package is currently slightly broken due to a recent incomplete refactor (it fails to run inference correctly due to a matrix alignment issue or bug). 

Your objectives:
1. **Fix the Vendored Package**: Inspect the source code of `fast_bayes_infer` at `/app/fast_bayes_infer/`, identify the bug in the log-likelihood calculation, fix it, and install the package in your environment.
2. **Find the Threshold**: We have provided a labeled training dataset at `/app/data/train.csv` containing both `clean` and `evil` records. Use the fixed `fast_bayes_infer.GaussianBayes` model to score these records. Perform cross-validation or statistical analysis to determine the optimal log-likelihood threshold that perfectly separates the clean data from the evil data.
3. **Build the ETL Filter**: Write a Python script at `/home/user/filter_pipeline.py` that processes a single CSV file, scoring each row using the Bayesian model and filtering out the anomalous records.

**Script Requirements**:
- Must be executable as: `python /home/user/filter_pipeline.py --input <input_csv_path> --output <output_csv_path>`
- The output CSV must retain the exact same headers as the input.
- The output CSV must contain *only* the rows that are classified as clean.
- The inference must be performant (utilizing the vectorized operations in `fast_bayes_infer`).

**Verification**:
We have an adversarial corpus to test your script:
- Clean dataset directory: `/app/data/clean/`
- Evil dataset directory: `/app/data/evil/`

Your script will be tested against these directories. To pass, your script must preserve 100% of the rows in the clean CSVs and reject 100% of the rows in the evil CSVs.