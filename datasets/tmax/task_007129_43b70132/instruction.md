You are a data analyst tasked with processing a batch of customer records and scoring them using a proprietary legacy model. 

You have been provided with two files:
1. `/home/user/customer_data.csv`: A raw dataset containing customer information.
2. `/home/user/model_config.json`: A JSON file containing the weights and architecture parameters for a logistic regression model.

Your objective is to clean the data, engineer the necessary features, reconstruct the model scoring logic, and output the predictions. Write a Python script to perform the following steps:

**1. Data Cleaning (Missing Values & Outliers):**
* Read `/home/user/customer_data.csv`.
* **`age` column**: Contains some data entry errors (e.g., negative values or unrealistically high values). Clip all `age` values to be strictly between 18 and 90, inclusive (i.e., values < 18 become 18, values > 90 become 90).
* **`income` column**: Contains missing values (NaN/empty). Impute all missing values using the **median** of the non-missing `income` values in the dataset.

**2. Feature Engineering:**
* Create a new feature called `combined_score` calculated as: `(score_A * 0.4) + (score_B * 0.6)`.
* Create a binary feature `income_bracket`: 1 if `income` > 60000, else 0.
* One-hot encode the `category` column (which contains values 'A', 'B', and 'C') into three binary columns (1 or 0): `cat_A`, `cat_B`, and `cat_C`.

**3. Model Reconstruction & Inference:**
* Parse `/home/user/model_config.json`. It contains an `"intercept"` and a `"weights"` dictionary.
* Calculate the linear combination `z` for each row using the exact feature names specified in the weights dictionary:
  `z = intercept + (weight_age * age) + (weight_combined * combined_score) + (weight_bracket * income_bracket) + (weight_catA * cat_A) + (weight_catB * cat_B) + (weight_catC * cat_C)`
* Apply the sigmoid activation function to get the probability: `prob = 1 / (1 + exp(-z))`
* Determine the binary class prediction: `class` is 1 if `prob >= 0.5`, otherwise 0.

**4. Output:**
* Save the results to `/home/user/results.csv`.
* The output CSV must contain exactly three columns in this order: `id`, `prob`, `class`.
* The `prob` column must be rounded to exactly 4 decimal places.
* The file must include a header row.