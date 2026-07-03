You are a Machine Learning Engineer responsible for preparing training data in a strictly controlled environment. You must write a Bash pipeline that handles model inference (generating pseudo-labels), bootstrap sampling, and reproducibility testing, without relying on heavy ML frameworks like PyTorch or Scikit-Learn.

You have been provided a dataset of raw numerical features at `/home/user/data/raw_features.csv`. 
The file contains 1000 lines. Each line has 4 comma-separated values: `user_id,x1,x2,x3`. There is no header.

Your task is to write a Bash script at `/home/user/build_dataset.sh` that takes two arguments:
1. `SEED` (an integer)
2. `EXPECTED_MD5` (a string representing an MD5 checksum)

When executed as `./build_dataset.sh <SEED> <EXPECTED_MD5>`, the script must perform the following steps:

**Phase 1: Model Architecture Inference (Pseudo-Labeling)**
Process `raw_features.csv`. For each row, calculate a score using the following linear model weights:
`Score = 0.5 * x1 - 1.2 * x2 + 0.8 * x3 + 0.1`

Determine a pseudo-label `L`:
- If `Score > 0`, `L = 1`
- If `Score <= 0`, `L = 0`

Create an intermediate file `/home/user/data/scored_features.csv` where each line contains 6 comma-separated values: `user_id,x1,x2,x3,Score,L`. Format the `Score` to exactly 4 decimal places (e.g., `0.1230`).

**Phase 2: Reproducible Bootstrap Sampling**
Create a bootstrap sample (sampling with replacement) of exactly 100 rows from `scored_features.csv` and save it to `/home/user/data/train_bootstrap.csv`.
To guarantee cross-platform reproducibility without relying on varying `shuf` or `awk` `rand()` implementations, you must implement a Linear Congruential Generator (LCG) to select the row indices.
Use the following parameters:
- Initial state `S = SEED`
- Multiplier `a = 1103515245`
- Increment `c = 12345`
- Modulus `m = 2147483648` (which is 2^31)

For `i` from 1 to 100:
1. Update state: `S = (a * S + c) % m`
2. Pick row index: `Index = (S % 1000) + 1` (This gives an index between 1 and 1000 inclusive).
3. Append the corresponding row from `scored_features.csv` to `/home/user/data/train_bootstrap.csv`.

**Phase 3: Pipeline Reproducibility Testing**
Calculate the standard MD5 checksum of `/home/user/data/train_bootstrap.csv` (just the hash, no file paths).
Compare it to the `EXPECTED_MD5` provided as the second argument.
- If they match exactly, print strictly the word `REPRODUCIBLE` to standard output.
- If they do not match, print strictly `DIVERGENT` to standard output.

**Constraints:**
- The script must be executable (`chmod +x`).
- Write the logic primarily using Bash, `awk`, and standard GNU coreutils (`bc`, `sed`, etc.). You may use inline Python strictly only if needed for large integer math, but a pure Bash/AWK solution is preferred.
- Make sure to clear or overwrite `/home/user/data/scored_features.csv` and `/home/user/data/train_bootstrap.csv` if the script runs multiple times.

Before you begin, verify that `/home/user/data/` exists and contains `raw_features.csv`.