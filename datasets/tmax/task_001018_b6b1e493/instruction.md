You are an MLOps engineer tasked with setting up a robust experiment tracking pipeline for a text classification task. Your goal is to evaluate a custom tokenization package, train a model, and compute confidence intervals using bootstrap sampling. You will need to write both Python and R code to complete this end-to-end workflow.

**Step 1: Fix and Install the Vendored Package**
We have a proprietary text processing package located at `/app/vendored/fast_vocab-1.2.3`. 
Currently, the package is broken due to a syntax error in its main tokenization module and a typo in its `setup.py`. 
Identify and fix the perturbations, then install the package into your Python environment so that `import fast_vocab` works successfully.

**Step 2: Tokenization and Dataset Preparation (Python)**
A dataset is located at `/app/data/dataset.csv` with two columns: `text` and `label`.
Write a Python script `/home/user/train_evaluate.py` that:
1. Loads the dataset.
2. Uses the `fast_vocab.tokenize(text)` function to tokenize the text column (it returns a string of space-separated tokens).
3. Converts the tokenized text into a TF-IDF matrix using `sklearn.feature_extraction.text.TfidfVectorizer`.

**Step 3: Model Training and Bootstrap Evaluation (Python)**
In the same Python script:
1. Train a Logistic Regression model on the entire TF-IDF matrix.
2. Generate 200 bootstrap samples (draw samples with replacement, same size as the original dataset).
3. For each bootstrap sample, calculate the accuracy of the trained model on the **Out-Of-Bag (OOB)** samples (the instances not included in that specific bootstrap draw).
4. Save the 200 OOB accuracy scores to a text file at `/home/user/oob_accuracies.csv` (one float per line).

**Step 4: Statistical Reporting (R)**
Write an R script `/home/user/calculate_ci.R` that:
1. Reads `/home/user/oob_accuracies.csv`.
2. Computes the `mean`, `ci_lower` (2.5th percentile), and `ci_upper` (97.5th percentile) of the OOB accuracies.
3. Outputs these metrics into a valid JSON file at `/home/user/experiment_results.json` with keys `"mean"`, `"ci_lower"`, and `"ci_upper"`.

Run your pipeline so that `/home/user/experiment_results.json` is generated. Your final model's mean OOB accuracy must meet our baseline metric threshold to be considered successful.