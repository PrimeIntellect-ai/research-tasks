You are an automation specialist tasked with building a robust data processing pipeline for employee survey results. The raw data is messy, contains Personal Identifiable Information (PII), and requires transformation before analysis.

You must orchestrate this pipeline using a `Makefile` to define a Directed Acyclic Graph (DAG) of tasks. Each step must be implemented using Python (`pandas` is permitted and recommended) and executed via the Makefile.

**Input Data:**
The raw data is located at `/home/user/raw_survey.csv`. 
It is a comma-separated file with the following columns: `id,name,email,department,q1,q2,q3,feedback`

**Pipeline Steps (Makefile Targets):**

1. **Target `clean`:**
   - Reads `/home/user/raw_survey.csv`.
   - The `feedback` column sometimes contains embedded newline characters (`\n`). You must **drop** any row where the `feedback` field contains an embedded newline.
   - Outputs the result to `/home/user/cleaned.csv`.

2. **Target `reshape`:**
   - Reads `/home/user/cleaned.csv`.
   - Reshapes the data from wide to long format. The columns `q1`, `q2`, and `q3` should be melted into two new columns: `question` (containing the strings 'q1', 'q2', 'q3') and `score` (containing the numeric scores).
   - Some scores are missing (NaN). **Impute** all missing values in the `score` column with the *overall mean* of the available `score` values across the entire dataset. Round the imputed values to 1 decimal place.
   - Outputs the result to `/home/user/reshaped.csv`.

3. **Target `anonymize`:**
   - Reads `/home/user/reshaped.csv`.
   - Replaces all values in the `name` column with the exact string `REDACTED`.
   - Replaces all values in the `email` column with the SHA256 hex digest of the *lowercase* email address.
   - Outputs the result to `/home/user/anonymized.csv`.

4. **Target `sample`:**
   - Reads `/home/user/anonymized.csv`.
   - Performs stratified sampling based on the `department` column. Select exactly 50% (`frac=0.5`) of the rows for each department.
   - You must use `random_state=42` in your sampling function to ensure reproducible output.
   - Outputs the result to `/home/user/final_sample.csv`.

5. **Target `all`:**
   - Defines the default execution that runs the entire DAG (`clean` -> `reshape` -> `anonymize` -> `sample`) in the correct dependency order.

**Deliverables:**
Create the Python scripts required for each step and the `Makefile` in `/home/user/`. When finished, running `make all` in `/home/user/` must successfully execute the pipeline and produce `/home/user/final_sample.csv`.