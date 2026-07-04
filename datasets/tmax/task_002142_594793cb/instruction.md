You are an MLOps engineer responsible for maintaining our experiment tracking infrastructure. We are receiving corrupted and anomalous experiment metric logs ("artifacts") from some compute nodes, which are poisoning our downstream ML dashboards.

We need a robust data filter written in Rust to sanitize and classify these incoming artifacts.

Here is the situation:
1. We have a legacy anomaly-scoring oracle located at `/app/bin/stat_oracle`. This is a stripped, UPX-packed ELF binary. It takes a single argument (the path to a CSV file) and prints a float representing the "oracle stability score" of the experiment to standard output.
2. The incoming artifacts are CSV files containing experiment metrics, primarily a column named `loss`. These files often contain missing values (empty strings or `NaN`) and extreme outliers due to sensor glitches.
3. The legacy `stat_oracle` is fragile and will crash or return garbage if fed files with missing values or extreme outliers.

Your objective is to create a Rust command-line tool that acts as a robust filter. 
Initialize your project at `/home/user/artifact_filter` (so the compiled binary will be at `/home/user/artifact_filter/target/release/artifact_filter`).

Your tool must accept a single command-line argument: the path to an artifact CSV file.
When processing a file, your tool must perform the following pipeline:
1. **Missing Value Handling**: Impute any missing values (empty strings or `NaN`) in the `loss` column with the median of the valid `loss` values in that file.
2. **Outlier Handling**: Remove any rows where the `loss` value is strictly greater than 3 standard deviations away from the mean of the imputed `loss` column.
3. **Bootstrapping**: Using the cleaned (imputed and outlier-filtered) `loss` data, perform a bootstrap resampling (1000 iterations, sampling with replacement) to compute the 95% confidence interval of the mean. Calculate the width of this interval (Upper Bound - Lower Bound).
4. **Oracle Integration**: Save the cleaned data to a temporary CSV file and pass it to `/app/bin/stat_oracle`. Read the float score it outputs.
5. **Classification**: 
   - If the bootstrap 95% CI width is `< 2.5` AND the oracle score is `> 0.65`, the artifact is valid. Print exactly `CLEAN` to standard output and exit with code `0`.
   - Otherwise, the artifact is anomalous. Print exactly `EVIL` to standard output and exit with code `1`.

We will verify your solution by compiling your Rust project in release mode and running it against two hidden datasets: a clean corpus and an adversarial corpus containing maliciously crafted experiment artifacts. 

Requirements:
- Your Rust tool must be fully self-contained in `/home/user/artifact_filter`.
- You may use external crates (e.g., `csv`, `serde`, `rand`, `statrs`, `polars`) by adding them to your `Cargo.toml`.
- Your final program must be compiled in release mode before you finish the task.