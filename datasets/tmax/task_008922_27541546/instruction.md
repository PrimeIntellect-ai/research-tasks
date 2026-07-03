You are a data analyst tasked with building a C++ data pipeline to validate a simple predictive model using bootstrap sampling.

You have been provided with a dataset at `/home/user/data.csv` containing historical data for a product. The CSV has a header row and three columns:
`marketing_spend`, `website_visits`, `actual_sales`

We have a pre-trained linear regression model. The model predicts sales based on the following formula:
`predicted_sales = 2.5 * marketing_spend + 1.2 * website_visits + 10.0`

Your task is to write and execute a C++ program (`/home/user/analyze.cpp`) that performs the following steps:

1. **ETL & Inference**: Read the CSV file, ignoring the header. For each row, calculate the `predicted_sales` using the model formula. Calculate the squared error `(actual_sales - predicted_sales)^2` for each row.
2. **Original MSE**: Calculate the Mean Squared Error (MSE) of the entire original dataset.
3. **Bootstrap Sampling**: Perform 1000 bootstrap iterations to estimate the 95% confidence interval of the MSE. 
    - For each iteration, create a bootstrap sample by drawing `N` times with replacement from the original dataset (where `N` is the total number of rows in the CSV).
    - Calculate the MSE for this bootstrap sample.
    - **Crucial**: To ensure reproducibility, use C++'s `<random>` library. Initialize the generator exactly like this before the loop:
      `std::mt19937 gen(42);`
      `std::uniform_int_distribution<int> dist(0, N - 1);`
      In your iteration, draw each index using `dist(gen)`. Collect the `N` indices, then compute the MSE for that sample.
4. **Confidence Interval**: Store the 1000 bootstrap MSE values and sort them in ascending order. 
    - The lower bound of the 95% CI will be the value at index 25 (0-indexed).
    - The upper bound of the 95% CI will be the value at index 975 (0-indexed).
    - Also calculate the mean of these 1000 bootstrap MSE values.

Output the final results to `/home/user/results.txt` in the following exact format (rounded to 4 decimal places):
```
Original MSE: <value>
Bootstrap Mean MSE: <value>
95% CI Lower: <value>
95% CI Upper: <value>
```

Compile your code with `g++ -O3 /home/user/analyze.cpp -o /home/user/analyze` and run it to produce the `results.txt` file.