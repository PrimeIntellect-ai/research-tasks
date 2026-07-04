You are an IT support technician. You have been assigned Ticket #8492. 

The data engineering team has a Bash-based data processing pipeline located in `/home/user/ticket_8492/`. The pipeline reads a CSV file of financial transactions, calculates per-user statistics (count, average, and population variance of transaction amounts), and loads the results into an SQLite database. Finally, a reporting script queries this database.

However, the pipeline is currently failing. The ticket reports:
1. **Assertion Failures**: The main processing script (`/home/user/ticket_8492/process.sh`) halts with an assertion failure complaining about "Negative variance detected". This is a mathematical impossibility for variance, suggesting a numerical instability issue in the naive formula used in the script.
2. **Incorrect Query Results**: The reporting script (`/home/user/ticket_8492/report.sh`) has a bug in its SQL query. It is supposed to output all users who have an average transaction amount greater than 100, but it is currently returning an empty or incorrect list due to a logic error in the SQL string inside the bash script.

Your task:
1. Comprehend the existing codebase in `/home/user/ticket_8492/`.
2. Fix the numerical instability in `process.sh`. The script currently computes population variance using the single-pass naive formula (E[X^2] - E[X]^2), which suffers from catastrophic cancellation for large numbers with small differences. Modify the `awk` block inside `process.sh` to use a numerically stable method (such as a two-pass algorithm or Welford's algorithm) to compute the exact population variance.
3. The script contains a validation function `assert_non_negative`. Ensure your fix passes this assertion.
4. Fix the query logic inside `report.sh` so that it correctly selects `user_id`, `avg_amount`, and `variance` from the `user_stats` table where `avg_amount > 100.0`.
5. Run `./process.sh` to populate the database.
6. Run `./report.sh > /home/user/ticket_8492/final_report.txt`.

The final output must be written to `/home/user/ticket_8492/final_report.txt` in a comma-separated format (no headers): `user_id,avg_amount,variance`. The variance should be rounded to 4 decimal places in the final report.

Ensure all scripts are executable and work correctly. Do not change the database schema or the names of the files.