You are acting as an MLOps engineer responsible for setting up an automated artifact tracking pipeline. We collect metadata from our dataset preparation, cross-validation, and hyperparameter tuning stages. Unfortunately, upstream experiment runs sometimes inject corrupted or maliciously malformed configuration artifacts into our system, which crashes our numerical downstream libraries. 

Your objective is to build a C++ CLI tool that sanitizes and validates incoming JSON experiment artifacts. 

Step 1: Environment & Package Setup
We have vendored a lightweight C++ JSON parser, `json11` (v1.0.0), located at `/app/json11`. 
However, the previous engineer left it in a broken state and it currently fails to compile. 
1. Fix the build configuration in `/app/json11/Makefile` so that running `make` successfully builds the static library `libjson11.a`.

Step 2: Build the Artifact Validator
Write a C++ program at `/home/user/artifact_validator.cpp` that parses a JSON file path provided as its first command-line argument. Compile it to `/home/user/artifact_validator`, statically linking against `/app/json11/libjson11.a`.

The validator must strictly enforce the following data science constraints to handle missing values, outlier configurations, and dataset preparation settings:
1. The JSON must successfully parse.
2. It must contain a top-level string field `experiment_id`.
3. It must contain a `metrics` object with:
   - `cv_folds`: an integer strictly >= 2 (for valid cross-validation).
   - `outlier_threshold_z`: a numerical float value between 1.0 and 5.0 inclusive (to prevent aggressive or negative outlier trimming).
4. It must contain a `tokenization` object with:
   - `vocab_size`: an integer >= 1000.
If ALL constraints are met, the program must exit with code `0`. If ANY constraint is violated, or if fields are missing/wrong type, the program must print an error to stderr and exit with code `1`.

Step 3: Verification Script
We have a set of artifacts in `/app/corpora`.
Write a bash script at `/home/user/run_validation.sh` that iterates over all files in `/app/corpora/clean/` and `/app/corpora/evil/`, running your `artifact_validator` on each. 
Your script should create two directories: `/home/user/accepted/` and `/home/user/rejected/`, and copy the files into the respective directories based on the exit code of your validator.