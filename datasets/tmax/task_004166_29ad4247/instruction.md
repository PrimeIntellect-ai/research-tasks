You are an AI assistant helping a data analyst process inference performance logs to understand system bottlenecks.

We have a dataset located at `/home/user/inference_logs.csv` containing performance metrics for a simulated ML inference engine. The dataset has the following columns:
- `Run_ID`: Unique identifier for the benchmark run.
- `Model_Type`: Either 'Vision' or 'NLP'.
- `CPU_Util`: CPU utilization percentage.
- `Mem_Util`: Memory utilization percentage.
- `Net_Lat`: Network latency in ms.
- `IO_Wait`: I/O wait time percentage.
- `Inference_Time_ms`: Total inference latency in ms.

Your task is to analyze this dataset using Python. You will need to set up your own virtual environment in `/home/user/venv`, install necessary data science packages (`pandas`, `scikit-learn`, `scipy`), and write a Python script to compute the following metrics:

1. **Dimensionality Reduction & Correlation**:
   - Extract the four system metrics: `CPU_Util`, `Mem_Util`, `Net_Lat`, and `IO_Wait`.
   - Standardize these four columns using `sklearn.preprocessing.StandardScaler`.
   - Apply Principal Component Analysis (PCA) using `sklearn.decomposition.PCA` with `n_components=1` (use `random_state=42` if applicable) to reduce these four metrics into a single feature: `System_Load_Index`.
   - Calculate the absolute value of the Pearson correlation coefficient between `System_Load_Index` and `Inference_Time_ms`.

2. **Hypothesis Testing**:
   - Conduct a two-sided Welch's t-test (independent t-test with unequal variances) to compare the `Inference_Time_ms` of 'Vision' models versus 'NLP' models.
   - Extract the resulting p-value.

Finally, output your results to a JSON file located precisely at `/home/user/analysis_results.json`. The JSON file must have exactly this structure, with floats rounded to 4 decimal places:

```json
{
  "abs_correlation": <float>,
  "ttest_p_value": <float>
}
```

Ensure all paths are absolute and correct. Your solution should handle the setup, data loading, statistical calculations, and JSON generation.