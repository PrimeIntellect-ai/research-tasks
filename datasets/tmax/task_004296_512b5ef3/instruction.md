You are a Machine Learning Engineer preparing training data for a user behavior model. You need to build a data preparation pipeline in C that cleans a raw dataset, handles missing values using a fixed Bayesian prior, caps outliers, and computes a similarity metric against a reference profile.

Your task:
1. There is a raw dataset located at `/home/user/raw_data.csv` with the following columns: `user_id`, `engagement_score`, `session_duration`, `bounce_rate`.
2. Write a C program at `/home/user/prepare_data.c` that reads this CSV file and applies the following transformations:
   - **Missing Value Handling**: If `engagement_score` is missing (empty string before the comma), impute it using a Bayesian prior mean of `0.50`.
   - **Outlier Handling**: If `session_duration` is greater than `1000.0`, cap it exactly at `1000.0`.
   - **Similarity Search / Feature Creation**: Compute the Euclidean distance of each user's features (`engagement_score`, `session_duration`, `bounce_rate`) against a reference "ideal user" profile: `engagement_score = 0.80`, `session_duration = 300.0`, `bounce_rate = 0.20`.
3. The C program must output the processed data to `/home/user/clean_data.csv`. The output CSV must have the header `user_id,engagement_score,session_duration,bounce_rate,distance`.
4. All floating-point numbers in the output CSV must be formatted to exactly two decimal places (e.g., `%.2f`).
5. Create a shell script `/home/user/run_pipeline.sh` that compiles `prepare_data.c` (using `gcc -lm`) and runs the executable to guarantee pipeline reproducibility.

Constraints:
- You must use standard C libraries (`stdio.h`, `stdlib.h`, `string.h`, `math.h`).
- Do not use external libraries.
- The input file will use standard Unix line endings (`\n`) and comma-separated values.