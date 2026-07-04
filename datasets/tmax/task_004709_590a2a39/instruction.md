You are a Machine Learning Engineer working on an edge device where a Python environment is currently broken (similar to a matplotlib environment misconfiguration, our Python runtime is throwing fatal errors). You urgently need to validate a linear model's performance on newly collected data. You are restricted to using only standard POSIX tools (`bash`, `awk`, `sed`, `grep`, `coreutils`, etc.).

All your work should be done in `/home/user/edge_ml/`.

The system has provided you with two files:
1. `/home/user/edge_ml/raw_data.csv`: A comma-separated file containing the latest collected data. The expected schema is:
   `id,f1,f2,f3,f4,f5,true_label`
   Unfortunately, the data ingestion pipeline has issues. Some rows have missing columns, extra columns, or non-numeric values (like "NaN", "null", or stray strings) in the feature or label columns.
2. `/home/user/edge_ml/model_weights.txt`: A text file containing the linear model's parameters. The first line is the bias term ($b$). The next 5 lines are the feature weights ($w_1$ to $w_5$).

Your task is to build a pure Bash/Awk pipeline that accomplishes the following three stages:

**Stage 1: Data Schema Enforcement**
Create a script `/home/user/edge_ml/1_clean.sh` that reads `raw_data.csv` and writes valid rows to `/home/user/edge_ml/clean_data.csv`.
A valid row MUST:
- Have exactly 7 comma-separated columns.
- Have purely numeric values (integers or floating-point numbers, possibly negative) for columns 2 through 7.
- Have an integer in column 1 (`id`).

**Stage 2: Model Output Validation (Linear Algebra)**
Create a script `/home/user/edge_ml/2_predict.sh` that applies the linear model to `clean_data.csv`.
- The linear model equation is: $\text{Prediction} = b + \sum_{i=1}^{5} (f_i \times w_i)$
- It must read the parameters from `model_weights.txt`.
- It must output to `/home/user/edge_ml/predictions.csv` with the format `id,prediction` (rounded to 4 decimal places).

**Stage 3: Covariance Analysis**
Create a script `/home/user/edge_ml/3_evaluate.sh` that computes the population covariance between the model's predictions and the `true_label` from `clean_data.csv`.
- The formula for population covariance is: $Cov(X, Y) = \frac{1}{N} \sum_{i=1}^{N} (X_i - \bar{X})(Y_i - \bar{Y})$
- It should read `predictions.csv` and `clean_data.csv`.
- It must output only the final covariance value (rounded to 4 decimal places) to `/home/user/edge_ml/covariance.txt`.

Ensure your scripts have execute permissions. Run them in sequence to produce the final `clean_data.csv`, `predictions.csv`, and `covariance.txt`.