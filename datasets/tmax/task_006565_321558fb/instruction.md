You are a data engineer working on an ETL pipeline written in Rust. The pipeline extracts text logs, computes a simple keyword-based embedding, applies a logistic regression model, and outputs predictions.

Currently, the pipeline has a critical bug: it produces "blank" or zeroed-out embeddings for all logs, resulting in identical predictions for every row. 

Your task is to fix the ETL pipeline and add a model output validation step.

### Project Setup
- The Rust project is located at `/home/user/etl_pipeline`.
- The input data is at `/home/user/data/input.csv` (CSV format with header: `id,text`). Note that the `text` column contains strings that may include commas and are enclosed in quotes.
- The pipeline should write the processed outputs to `/home/user/data/output.csv`.

### Pipeline Specifications
1. **Embedding Computation**: For each log, compute a 5-dimensional feature vector. Each dimension represents the frequency (count) of specific keywords in the `text` field (case-insensitive). The keywords, in exact order, are:
   `["error", "fail", "timeout", "success", "connect"]`
2. **Model Architecture Inference**: Apply a logistic regression model.
   - Weights: `[1.2, 0.8, 0.5, -1.0, 0.3]` (corresponding to the keywords above)
   - Bias: `-0.5`
   - Calculate the logit: $z = \text{bias} + \sum (\text{weight}_i \times \text{feature}_i)$
   - Calculate probability: $P = \frac{1}{1 + e^{-z}}$
   - Prediction: `1` if $P > 0.5$, else `0`.
3. **Output**: Write to `/home/user/data/output.csv` with the header `id,prob,prediction`. The `id` must match the input, `prob` is the calculated probability (float), and `prediction` is the integer class (1 or 0).

### Validation Step
After generating the output, you must validate the output distribution.
Modify the Rust program to also compute:
1. The mean of all output probabilities ($\bar{x}$).
2. The 95% confidence interval for the mean probability.
   - Use the sample standard deviation ($s$) with $N-1$ degrees of freedom.
   - Use the z-score $1.96$ for the 95% confidence level.
   - $CI = \bar{x} \pm 1.96 \times \frac{s}{\sqrt{N}}$

Write these three values (mean, lower_bound, upper_bound) to `/home/user/metrics.txt` as a single comma-separated line (e.g., `0.4501,0.4102,0.4900`).

Fix the code in `/home/user/etl_pipeline`, compile it (e.g., `cargo run`), and ensure both `/home/user/data/output.csv` and `/home/user/metrics.txt` are correctly generated. You may add external crates like `csv` to the `Cargo.toml` if needed to correctly parse the CSV file.