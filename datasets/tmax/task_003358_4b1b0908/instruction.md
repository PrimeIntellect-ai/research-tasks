You are an MLOps engineer tasked with migrating away from a legacy compiled tool used to track and score experiment artifacts. 

The legacy tool is located at `/app/legacy_scorer`. It is a stripped binary that reads tabular data of experiment artifacts, aggregates three continuous metrics, and applies a Bayesian updating calculation to compute a posterior probability score based on a given prior.

Your task is to write a Bash script at `/home/user/scorer.sh` that perfectly replicates the behavior, math, and output format of this legacy binary. Your script must serve as a drop-in replacement. You may use standard Unix text processing and math tools (like `awk`, `sed`, `bc`) within your Bash script, but you must not use Python, Perl, or other higher-level scripting languages.

**Arguments:**
Both the legacy binary and your script must accept arguments in this exact format:
`--prior <float> <csv_file>`

**Input CSV Format:**
The input CSV is headerless. Each row represents one artifact and contains four comma-separated columns:
`artifact_id,metric_a,metric_b,metric_c`
(The metrics are continuous values between 0.0 and 1.0).

**Output Format:**
The tool must print to standard output one line per artifact in the format:
`artifact_id,posterior_score`
(The score is printed to 6 decimal places).

**Requirements:**
1. You must reverse-engineer the aggregation weights and the probabilistic formula by treating `/app/legacy_scorer` as a black-box oracle and observing its outputs for various inputs.
2. Your script `/home/user/scorer.sh` must be executable (`chmod +x`).
3. The output of your script must be bit-exact equivalent to the binary for any valid inputs.
4. Your solution should gracefully handle processing tabular data efficiently using standard Bash/Awk tooling.

To succeed, you will need to construct test inputs, query the binary, infer the statistical transformations it performs, and implement an equivalent transformation pipeline in `/home/user/scorer.sh`.