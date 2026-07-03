You are an MLOps engineer tracking the numerical stability of an experimental text embedding extraction pipeline. You need to evaluate the variance of corpus-level semantic features under dataset perturbation using bootstrap sampling.

Your task is to write a Python script `/home/user/scripts/evaluate_stability.py` that processes a text corpus, extracts a specific linear algebraic feature, and computes its bootstrap confidence intervals. 

Here are the precise specifications for your pipeline:

**1. Data Preparation & Tokenization:**
- Read the text file `/home/user/data/corpus.txt`. Each line represents one document.
- Tokenize the documents: convert the text to lowercase and split by whitespace (using Python's standard string `.split()`).
- Build a global vocabulary of all unique tokens across the entire original corpus, sorted alphabetically. 

**2. Base Evaluation (Linear Algebra):**
- Construct a Term-Document Matrix (TDM) for the corpus. The matrix should have shape `(V, D)`, where `V` is the size of the global vocabulary and `D` is the number of documents.
- `TDM[i, j]` should be the raw frequency (count) of the `i`-th vocabulary word in the `j`-th document.
- Compute the top (largest) singular value of this TDM.

**3. Bootstrap Sampling:**
- Set the random seed: `numpy.random.seed(42)`.
- Perform `N = 100` bootstrap iterations.
- In each iteration, create a bootstrap sample of the documents by drawing `D` documents from the original corpus *with replacement* using `numpy.random.choice(D, size=D, replace=True)`.
- For each bootstrap sample, compute the TDM using the *same global vocabulary* established in step 1.
- Compute the top singular value for this bootstrap TDM and store it.

**4. Artifact Logging (Numerical Accuracy):**
- Calculate the mean of the 100 bootstrap singular values.
- Calculate the 95% confidence interval for the top singular value using the percentile method (compute the 2.5th and 97.5th percentiles of the bootstrap singular values using `numpy.percentile`).
- Save the results to `/home/user/artifacts/run_metrics.json` with the following schema:
  ```json
  {
      "vocab_size": <int>,
      "original_top_sv": <float>,
      "bootstrap_mean_sv": <float>,
      "ci_lower": <float>,
      "ci_upper": <float>
  }
  ```
- All float values in the JSON must be rounded to exactly 4 decimal places.

**Environment Setup:**
- The corpus is located at `/home/user/data/corpus.txt`.
- You must create the output directory `/home/user/artifacts/` if it does not exist.
- Standard libraries like `numpy` and `scipy` are available.

Execute the script and ensure the JSON artifact is generated correctly.