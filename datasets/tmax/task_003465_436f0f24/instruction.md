You are an MLOps engineer tasked with tracking and validating experiment artifacts from different language model runs. You have a set of golden reference outputs and outputs from two different experimental models.

Your workspace contains:
- `/home/user/golden.csv`: Golden reference standard outputs.
- `/home/user/exp_A.csv`: Outputs from Experiment A.
- `/home/user/exp_B.csv`: Outputs from Experiment B.

Your task is to write and execute a Python script `/home/user/analyze.py` that performs the following steps:
1. **Embedding Computation & Retrieval**: Use `sklearn.feature_extraction.text.TfidfVectorizer` (with default parameters) to represent the texts. **Fit** the vectorizer ONLY on the `text` column of `golden.csv`. Then, **transform** the `text` columns of `exp_A.csv` and `exp_B.csv` using this fitted vectorizer.
2. **Model Output Validation**: For every text in `exp_A.csv` and `exp_B.csv`, compute its cosine similarity against ALL vectors from `golden.csv`. The "validation score" for an experiment text is the **maximum** cosine similarity it achieves with any golden text.
3. **Hypothesis Testing**: Perform a Welch's two-sample t-test (two-sided) to determine if there is a statistically significant difference between the mean validation scores of Experiment A and Experiment B.
4. **Bayesian Inference**: Define a "success" for a model output as having a validation score strictly greater than `0.5` (`score > 0.5`). Assume the success probability of Experiment A follows a Binomial distribution. Using a Beta prior with parameters $\alpha=1, \beta=1$, calculate the parameters of the posterior Beta distribution for the success rate of Experiment A.
5. **Reporting**: Output the final results to `/home/user/report.json` with exactly these keys (and float/integer values):
```json
{
  "t_stat": <float, the test statistic from the t-test>,
  "p_value": <float, the p-value from the t-test>,
  "exp_A_success_alpha": <int or float, the posterior alpha parameter for Exp A>,
  "exp_A_success_beta": <int or float, the posterior beta parameter for Exp A>
}
```

**Notes:**
- You may need to install necessary packages (like `pandas`, `scikit-learn`, `scipy`) using `pip`.
- Use `scipy.stats.ttest_ind` with `equal_var=False` for the Welch's t-test.
- Ensure the JSON file is valid and correctly formatted.