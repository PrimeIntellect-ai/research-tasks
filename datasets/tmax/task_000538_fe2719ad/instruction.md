You are a data analyst building a reproducible similarity recommendation pipeline in C. You need to process a dataset of user ratings and find the most similar user based on the Pearson correlation coefficient.

A dataset has been provided at `/home/user/ratings.csv`. The file has no header. Each line represents a user. The first comma-separated value is the `user_id` (an integer), and the subsequent 5 values are floating-point ratings for 5 different items. 

Your task is to create a complete, reproducible C-based pipeline to find the most similar user to a target user. 

Perform the following steps:
1. Write a C program named `/home/user/recommender.c` that:
   - Takes a single command-line argument: the target `user_id` (integer).
   - Reads `/home/user/ratings.csv`.
   - Computes the Pearson correlation coefficient between the target user and all other users across the 5 items.
   - Finds the user with the highest correlation (excluding the target user themselves).
   - Writes the result to `/home/user/top_match.txt` in the exact format: `Match: [user_id], Score: [correlation_score]`, where the correlation score is formatted to exactly 4 decimal places (e.g., `Match: 3, Score: 0.8521`). If multiple users have the same highest score, pick the one with the lowest `user_id`.

2. Write a `/home/user/Makefile` that:
   - Has a `default` target that compiles `recommender.c` into an executable named `recommender`.
   - Links the math library (`-lm`).
   - Has a `clean` target that removes the executable.

3. Write a bash script `/home/user/run_pipeline.sh` that:
   - Cleans the build environment (calls `make clean`).
   - Builds the program (calls `make`).
   - Runs the program targeting user ID `1`.

Make sure `/home/user/run_pipeline.sh` is executable. You should execute your pipeline script to ensure it generates the `top_match.txt` file correctly. 

Note: The Pearson correlation coefficient $r$ between two arrays $x$ and $y$ of length $n$ is calculated as:
$r = \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum (x_i - \bar{x})^2 \sum (y_i - \bar{y})^2}}$
where $\bar{x}$ and $\bar{y}$ are the sample means. If the denominator is 0, the correlation is defined as 0.0.