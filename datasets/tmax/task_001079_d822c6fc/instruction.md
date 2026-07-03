We are currently modernizing our ETL pipeline and migrating away from legacy compiled binaries. One critical component is a proprietary data quality scoring tool located at `/app/legacy_score`. This stripped binary accepts a JSON string containing four numeric features and outputs a floating-point data quality score. 

The vendor went out of business, so we do not have the source code. However, our data science team has mathematically proven that the binary's underlying logic is a 2nd-degree polynomial regression over the four input features (with no degree-3 or higher terms, and no non-linear transformations like log or exponential).

Your task is to build a reproducible, Python-based drop-in replacement for our new ETL pipeline. 

Requirements:
1. **Black-box Sampling & Modeling**: Generate a sufficient sample of valid random inputs, pass them through `/app/legacy_score` to collect the ground-truth scores, and train a regression model to perfectly reverse-engineer the exact weights and coefficients used by the legacy binary.
2. **Schema Enforcement**: Create a Python script at `/home/user/etl_scorer.py`. This script must accept exactly one command-line argument: a JSON string. It must first enforce the data schema: the JSON must contain exactly four keys (`"f1"`, `"f2"`, `"f3"`, `"f4"`) and all values must be numbers (floats or integers). If the schema is invalid, print `SCHEMA_ERROR` and exit with code 1.
3. **Scoring**: If the schema is valid, your script must compute the score using the reverse-engineered mathematical formula and print *only* the resulting floating-point score to standard output, rounded to 4 decimal places.
4. **Reproducibility**: Ensure your mathematical replication is completely accurate. Do not rely on large pickeled machine learning models for the final script; extract the coefficients and hardcode the mathematical polynomial function in `/home/user/etl_scorer.py` so it runs instantaneously.

Example usage for your final script:
`python3 /home/user/etl_scorer.py '{"f1": 1.5, "f2": -2.0, "f3": 0.0, "f4": 3.1}'`

The automated test suite will aggressively fuzz both the legacy binary and your Python script with thousands of random payloads to ensure bit-exact behavioral equivalence.