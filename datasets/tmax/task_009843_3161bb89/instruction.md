You are acting as a data analyst who needs to build a lightweight, dependency-free Bash pipeline to process CSV files, enforce data schemas, and compute mathematical similarities. You must use standard Linux utilities (like `awk`, `sed`, `grep`, `sort`, `head`) and write your solution entirely in Bash. Python, R, or other higher-level languages are not allowed.

Your task is to create an analysis environment, validate a dataset, and build a similarity search tool.

**Step 1: Environment Setup**
Create a directory `/home/user/analysis`. All your scripts and output files should be saved here. 

**Step 2: The Data**
You are provided with a file at `/home/user/data/users.csv`. It contains user feature vectors.
The expected schema is:
- A header row: `user_id,f1,f2,f3,f4`
- Exactly 5 columns per row, comma-separated.
- `user_id` must start with an uppercase `U` followed by digits (e.g., `U10`).
- Columns `f1` through `f4` must be numbers (integers or floats).

**Step 3: Schema Enforcement & Filtering**
Write a script `/home/user/analysis/recommend.sh` that takes one argument: a Target User ID (e.g., `U1`).
When the script runs, it must first validate `users.csv`. 
- Any data row that violates the schema (wrong number of columns, invalid user_id format, or non-numeric features) must be skipped.
- Write the raw, skipped lines (excluding the header) to `/home/user/analysis/invalid_rows.log`.

**Step 4: Similarity Search (Mathematical)**
For the Target User ID passed as the argument:
1. Find their feature vector among the *valid* rows. If the target user is invalid or not found, exit with code 1.
2. Calculate the Euclidean distance between the Target User and every *other* valid user in the dataset. 
   *(Formula: sqrt((f1_a - f1_b)^2 + (f2_a - f2_b)^2 + (f3_a - f3_b)^2 + (f4_a - f4_b)^2))*
3. Find the 3 most similar users (those with the lowest Euclidean distance to the target user).
4. Save these top 3 recommendations to `/home/user/analysis/recommendations.txt` in the format:
   `user_id,distance`
   Sort them by distance ascending. Round the distance to exactly 3 decimal places.

**Testing**
To complete the task, ensure your script is executable and run it for the user `U1`:
`/home/user/analysis/recommend.sh U1`

Make sure `/home/user/analysis/invalid_rows.log` and `/home/user/analysis/recommendations.txt` are generated correctly according to the specifications.