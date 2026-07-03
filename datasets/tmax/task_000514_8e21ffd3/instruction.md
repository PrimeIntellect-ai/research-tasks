You are acting as a data engineer building a validation step for an ETL pipeline. We need a fast C++ utility to read a raw dataset, enforce a strict schema, tokenize text, and calculate statistical confidence intervals to detect data drift in token lengths.

Write a C++ program and save it as `/home/user/etl_stats.cpp`. 

Your program must do the following:
1. **Schema Enforcement**: Read a CSV file located at `/home/user/raw_data.csv`. The expected schema is strictly `id,text` where `id` must be an integer, and `text` is a string containing space-separated words. If a row does not strictly match this schema (e.g., the `id` cannot be parsed as a valid integer, or there is no comma), your program must completely ignore that row and move to the next.
2. **Tokenization**: For every valid row, tokenize the `text` field by splitting on single space characters (` `). 
3. **Dataset Preparation & Calculation**: Calculate the string length (number of characters) of every token extracted from the valid rows. Treat all token lengths from all valid rows as a single sample.
4. **Hypothesis Testing (Confidence Intervals)**: Calculate the sample mean and the 95% Confidence Interval for the mean token length across the entire valid dataset. 
   - Use $Z = 1.96$ for the 95% confidence level. 
   - Use the sample standard deviation (i.e., divide by $n-1$ for variance) to compute the standard error.
5. **Output**: Write the results to a text file at `/home/user/etl_report.txt` with exactly the following format (numerical accuracy matters, format to exactly 4 decimal places):
   ```
   Mean: <mean_value>
   CI: [<lower_bound>, <upper_bound>]
   ```

You must write the code, compile it using `g++` (e.g., `g++ -O3 etl_stats.cpp -o etl_stats`), and run it so that `/home/user/etl_report.txt` is generated with the correct results.