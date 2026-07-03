You are an MLOps engineer tasked with tracking and benchmarking machine learning experiment artifacts. We have raw JSONL logs of model inference trials, and you need to process them, enforce a schema, and build a benchmarking script that estimates model reliability using Bayesian inference.

There is a vendored tool on the system that you must use to convert the logs, but it has a bug. Follow these steps:

1. **Fix the Vendored Package:**
   There is a package at `/app/json2csv-schema-1.2` which converts JSONL experiment logs into a strict CSV schema. 
   However, the package is slightly broken. Its `Makefile` has a deliberate error preventing standard installation, and the main executable `json2csv.sh` has incorrect line endings (CRLF) and lacks execution permissions.
   Fix the package so that running `make install PREFIX=/home/user/.local` successfully installs the `json2csv` binary to `/home/user/.local/bin/json2csv`.

2. **Schema Enforcement & Transformation:**
   Using the fixed `json2csv` tool, convert the raw experiment logs located at `/home/user/raw_experiments.jsonl` to `/home/user/artifacts.csv`.
   The tool requires an environment variable `ENFORCE_STRICT_SCHEMA=1` to ensure missing fields are properly rejected.

3. **Bayesian Benchmarking Script:**
   Write a Bash script at `/home/user/bayesian_benchmark.sh` that takes exactly two arguments:
   - `$1`: `artifact_id` (e.g., `ART-101`)
   - `$2`: `latency_threshold` (integer, e.g., `50`)

   The script must:
   - Read `/home/user/artifacts.csv` (which has columns: `artifact_id,run_id,status,latency_ms`).
   - Find all rows matching the given `artifact_id`.
   - A trial is considered a **"success"** if `status` is exactly `SUCCESS` AND `latency_ms` is strictly less than or equal to `latency_threshold`.
   - A trial is a **"failure"** if it matches the `artifact_id` but does not meet the success criteria.
   - Perform a Bayesian update starting with a Beta prior where alpha=2, beta=2. 
   - Calculate the posterior mean probability of success: `Posterior_Mean = (2 + successes) / (4 + successes + failures)`.
   - Output ONLY this posterior mean rounded to exactly 4 decimal places (e.g., `0.6500`), followed by a newline.

Your script will be tested against a hidden reference implementation (oracle) using hundreds of random `artifact_id` and `latency_threshold` combinations to ensure bit-exact equivalence.