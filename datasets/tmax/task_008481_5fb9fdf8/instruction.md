You are a data analyst tasked with building a robust and reproducible A/B testing pipeline in Rust. 

You have been provided with a dataset at `/home/user/data.csv`. The CSV contains the following columns: `user_id`, `group` (either 'A' or 'B'), `session_duration` (in seconds), and `items_viewed` (integer).

Your task is to create a Rust project that processes this data, performs feature engineering, and conducts statistical hypothesis testing to evaluate if Group B performs significantly differently from Group A.

Specifically, you must:
1. Initialize a new Rust binary project at `/home/user/ab_test_pipeline`.
2. Read `/home/user/data.csv`.
3. Create a new engineered feature for each row called `engagement_score`, calculated as:
   `engagement_score = (session_duration * 0.5) + (items_viewed * 2.5)`
4. Separate the `engagement_score` data by `group` (A and B).
5. Compute the sample mean and sample variance for each group.
6. Perform a Welch's t-test (two-tailed, unequal variances) to test the null hypothesis that the two groups have the same mean `engagement_score`. Calculate the t-statistic and the p-value. (Use Mean B - Mean A for the difference).
7. Calculate the 95% Confidence Interval (CI) for the difference in means (`Mean B - Mean A`). 
8. Output the final statistics to a JSON file at `/home/user/results.json`. The JSON file must have exactly this structure, with all numeric values rounded to 4 decimal places:
   ```json
   {
     "mean_a": 12.3456,
     "mean_b": 15.6789,
     "t_statistic": 2.3456,
     "p_value": 0.0123,
     "ci_lower": 1.2345,
     "ci_upper": 4.5678
   }
   ```
9. To ensure pipeline reproducibility, you must write at least one unit test in your Rust code (`#[test]`) that takes a hardcoded small dataset (e.g., 3 rows for A, 3 rows for B) and asserts that the computed `t_statistic` matches a known expected value to within 0.001. Ensure `cargo test` runs successfully.

Compile and run your project so that `/home/user/results.json` is generated with the correct values derived from `/home/user/data.csv`.