You are a data analyst responsible for auditing our machine learning pipelines for data leakage. Specifically, we have had issues where analysts apply transformations (like scaling or whitening) to the entire dataset before splitting it into train and test sets, violating the core principle of pipeline reproducibility and independent evaluation.

We have gathered two corpora of dataset splits:
- `/home/user/data/clean/`: Contains 20 subdirectories (e.g., `dataset_001`, `dataset_002`, etc.), each holding a `train.csv` and a `test.csv`. These were processed correctly.
- `/home/user/data/evil/`: Contains 20 subdirectories, each holding a `train.csv` and a `test.csv`. These suffer from "Joint Whitening" leakage.

Your task is to build a detector that can automatically classify a dataset directory as clean or leaky.

**Step 1: Fix and Install the Vendored Dependency**
To perform high-speed covariance calculations, you must use our internal C-extension package `fast-covar`. 
The source code for version 1.2.0 is vendored at `/app/fast-covar-1.2.0`. 
However, the package was recently updated by a macOS user and currently fails to build/install on Linux due to a faulty environment check in its build configuration.
You must:
1. Identify and remove the deliberate perturbation preventing it from installing on Linux.
2. Install the package in your environment (e.g., `pip install -e /app/fast-covar-1.2.0`).

**Step 2: Data Schema Enforcement & Joining**
Write a Python CLI tool at `/home/user/detector.py` that takes a single directory path as a command-line argument.
The tool must:
1. Read `train.csv` and `test.csv` from the provided directory.
2. Enforce the data schema: Ignore any column named `id` or `target`. Keep only the continuous feature columns `feature_0` through `feature_9`. Drop any rows containing nulls.
3. Convert the filtered data into numeric matrices.

**Step 3: Leakage Detection via Linear Algebra**
Data leakage in the "evil" corpus occurred because the analyst applied a whitening transformation (forcing the covariance matrix to be the Identity matrix $I$) to the *concatenation* of the train and test sets, rather than fitting the transformation on the train set alone.
- If correctly processed (clean), the covariance of the **Train** set alone will be extremely close to the Identity matrix.
- If incorrectly processed (evil/leaky), the covariance of the **Concatenated (Train + Test)** set will be extremely close to the Identity matrix, while the Train set's covariance will deviate significantly from $I$.

Use the `fast_covar.compute_cov(matrix)` function (which expects a 2D numpy array and returns its covariance matrix) to calculate the necessary covariance matrices. 
Implement the mathematical logic to check these properties (accounting for minor floating-point inaccuracies, e.g., using a tolerance of `1e-4` for the Frobenius norm of the difference from $I$).

**Step 4: Classification**
Your script `/home/user/detector.py <dataset_dir>` must:
- Exit with code `0` if the dataset is classified as **CLEAN**.
- Exit with code `1` if the dataset is classified as **EVIL** (leaky).

Ensure your script is robust and correctly utilizes the fixed `fast-covar` package. You may use standard bash utilities and python to test your script against the provided corpora.