You are a data analyst tasked with building a high-performance data processing and statistical analysis pipeline in C++ without using external data science libraries (only the C++ Standard Library is allowed).

You have been provided with a dataset at `/home/user/transactions.csv`. It contains e-commerce transaction records with the following columns: `transaction_id`, `age`, `purchase_amount`, `review_text`, and `rating`.

Your goal is to write a C++ program (e.g., `/home/user/pipeline.cpp`) that reads this dataset and performs the following tasks:

1. **Tokenization & Feature Engineering**: 
   Process the `review_text` column. Tokenize the text by splitting on whitespace and stripping all punctuation. Create a new binary feature `has_good` which is `1` if the token "good" (case-insensitive) appears in the review, and `0` otherwise.

2. **Hypothesis Testing (Confidence Intervals)**:
   Group the data into two subsets based on `rating`: 
   - "Positive": `rating >= 4`
   - "Negative": `rating < 4`
   Calculate the 95% Confidence Interval for the mean `purchase_amount` for both groups. Use the sample standard deviation (divide by N-1) and a Z-value of `1.96`.
   Write the results to `/home/user/ci_results.csv` with the exact header `group,mean,lower_bound,upper_bound`. The groups should be named `Positive` and `Negative`. Format floats to 3 decimal places.

3. **Model Training**:
   Implement Simple Linear Regression (using Ordinary Least Squares) to predict `rating` (dependent variable, Y) based strictly on `purchase_amount` (independent variable, X) using the entire dataset.
   Write the calculated slope and intercept to `/home/user/model_results.txt` in the format:
   ```
   Slope: [value]
   Intercept: [value]
   ```
   Format floats to 3 decimal places.

Compile your code using `g++` and run it to generate the required output files. Let me know when you are done.