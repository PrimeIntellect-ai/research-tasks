You are an ML Engineer working on a C-based ETL pipeline that prepares collaborative filtering data for a recommendation system. The pipeline reads a CSV file of user-item interactions, but it has a subtle bug inspired by a classic pandas issue: it silently mishandles missing integer values, resulting in garbage float data leaking into the downstream similarity search matrix.

Your workspace in `/home/user/etl_project/` contains:
1. `interactions.csv`: A dataset with columns `user_id,item_id,rating`. Ratings are integers 1-5, but missing values are represented by `?`.
2. `etl.c`: A C program that reads the CSV and computes a basic metric. It uses `sscanf` which fails on `?`, causing the `rating` variable to retain uninitialized memory or the previous row's value.

Your task is to fix the pipeline, implement a Bayesian-smoothed imputation for missing values, and run a hyperparameter tuning script to track the experiments.

**Instructions:**
1. **Fix the Parsing Bug:** Modify `etl.c` to properly detect `?` as missing values instead of letting `sscanf` silently fail.
2. **Implement Bayesian Imputation:** For any missing rating for a user, impute it using the following formula:
   `imputed_rating = (user_known_rating_sum + alpha * global_avg) / (user_known_rating_count + alpha)`
   where `global_avg` is the average of all *known* ratings in the entire dataset. `alpha` is a hyperparameter provided via command-line argument (e.g., `./etl --alpha 2.0`). Calculate `global_avg` in a first pass, or compute it correctly based on the data. (For simplicity, assume max 1000 rows).
3. **Compile:** Compile your fixed code into an executable named `etl` in the same directory (use `gcc etl.c -o etl -lm`).
4. **Experiment Tracking:** Write a bash script `/home/user/etl_project/tune.sh` that iterates over the `alpha` values: `1.0`, `2.0`, `5.0`, and `10.0`. 
5. **Output Requirement:** For each run, the `etl` program should print exactly one line to stdout in this format:
   `Alpha: <alpha_value>, Total Imputed Sum: <sum_of_only_the_imputed_ratings_formatted_to_2_decimal_places>`
   Have `tune.sh` append these outputs to `/home/user/etl_project/experiment.log`.

Example of expected `experiment.log` format:
```
Alpha: 1.0, Total Imputed Sum: 8.50
Alpha: 2.0, Total Imputed Sum: 8.67
...
```

Ensure your C program efficiently computes the user-specific known rating sums and counts before doing the imputation pass. You may need to modify the C code to store rows in memory (a simple array of structs is fine since the dataset is small).