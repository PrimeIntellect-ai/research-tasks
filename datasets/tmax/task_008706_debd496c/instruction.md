You are assisting a computational researcher in organizing a newly collected dataset of sensor readings. The researcher needs an ETL pipeline to process the data, a custom script to run inference using an exported model's weights, and a statistical analysis using bootstrap sampling to evaluate confidence intervals.

Here is the step-by-step pipeline you need to build:

**1. Data Extraction and Load (ETL)**
The raw data is located at `/home/user/raw_data.csv`. It contains the following columns: `id`, `category`, `f1`, `f2`, `f3`. Some rows have missing values (empty strings) in the feature columns (`f1`, `f2`, `f3`).
Write a Python script that reads this CSV, drops any row that contains missing values in *any* of the feature columns, and loads the cleaned data into an SQLite database at `/home/user/sensor_data.db`. Create a table named `readings` with the same columns (ensure `id` is an integer, `category` is text, and `f1`, `f2`, `f3` are floats).

**2. Model Architecture Reconstruction and Inference**
The researcher previously trained a small neural network, but only saved the raw weights in `/home/user/weights.json`. 
The model is a Multilayer Perceptron (MLP) with the following architecture:
- Input layer: 3 features (`f1`, `f2`, `f3`)
- Hidden layer: 4 units, ReLU activation function: $f(x) = \max(0, x)$
- Output layer: 1 unit, Linear activation (no activation function)

The `weights.json` file contains a dictionary with keys: `W1`, `b1`, `W2`, `b2`.
Write a Python script that connects to `sensor_data.db`, fetches the cleaned features, and reconstructs this forward pass using standard mathematical operations (e.g., using `numpy`). Calculate the predicted output for each row. Update the `readings` table in your SQLite database to include a new float column named `prediction` containing these results.

**3. Statistical Aggregation (Bootstrap Sampling)**
Now the researcher wants to calculate the 95% confidence interval for the mean prediction of *each category* using bootstrap sampling.
Write a script that reads the predictions from the database and performs the following for each distinct `category` (sorted alphabetically):
- Use `numpy` to draw $B = 10,000$ bootstrap samples (sample with replacement) from the predictions of that category.
- Calculate the mean of each bootstrap sample.
- Determine the 95% confidence interval using the percentile method (2.5th and 97.5th percentiles using standard `numpy.percentile` defaults).

**Important constraints for reproducibility:**
- Set `numpy.random.seed(42)` exactly once, right before you start iterating over the sorted categories to perform the bootstrap sampling.

Save the final confidence intervals in a JSON file at `/home/user/summary.json`. The file should have the following format:
```json
{
  "CategoryA": [lower_bound, upper_bound],
  "CategoryB": [lower_bound, upper_bound]
}
```
Round the bounds to 4 decimal places.