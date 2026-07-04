You are a data analyst tasked with building a lightweight mathematical pipeline entirely in Bash (using standard tools like `awk`, `bc`, `sed`, etc., without relying on Python or R). 

Your objective is to process a CSV dataset, prevent a common data leakage issue (scaling leak), build a linear regression model from scratch, and evaluate it on a test set.

Here is the setup:
You have a dataset located at `/home/user/dataset.csv`. It contains two columns with headers: `Feature_X` and `Target_Y`.
There are exactly 100 data rows (plus 1 header row).

Your task is to write a bash script `/home/user/pipeline.sh` that does the following when executed:

1. **Dataset Preparation (Train/Test Split)**
   - Split the dataset into a training set (the first 80 data rows) and a test set (the last 20 data rows). 
   
2. **Feature Engineering (Z-Score Scaling)**
   - Calculate the mean ($\mu$) and population standard deviation ($\sigma$) of both `Feature_X` and `Target_Y` using **ONLY** the training set. (Population std uses $N$, not $N-1$).
   - *Crucial Data Leak Prevention:* Scale both the training set AND the test set using the $\mu$ and $\sigma$ calculated from the training set. 
   - The scaling formula is $Z = \frac{val - \mu}{\sigma}$.

3. **Model Reconstruction (Linear Regression)**
   - Using the scaled training data, compute the Ordinary Least Squares (OLS) linear regression parameters: slope ($m$) and intercept ($b$).
   - Since both variables are Z-score scaled, the intercept $b$ should theoretically be 0, and the slope $m$ will be the Pearson correlation coefficient. Calculate them explicitly.

4. **Inference & Evaluation**
   - Using your model ($Y_{pred} = m \cdot X_{scaled} + b$), predict the scaled `Target_Y` values for the scaled test set.
   - Calculate the Mean Squared Error (MSE) of these predictions against the actual scaled `Target_Y` test values.

5. **Reporting**
   - Your script must output a strictly formatted JSON file to `/home/user/results.json` containing the calculated statistics and final MSE, rounded to 4 decimal places.

The `/home/user/results.json` file must look exactly like this:
```json
{
  "train_mean_X": 0.0000,
  "train_std_X": 0.0000,
  "train_mean_Y": 0.0000,
  "train_std_Y": 0.0000,
  "model_m": 0.0000,
  "model_b": 0.0000,
  "test_mse": 0.0000
}
```

Constraints:
- You must create the `/home/user/pipeline.sh` script and ensure it is executable.
- Do NOT use Python, R, or any other high-level scripting language. Use standard Unix utilities (`bash`, `awk`, `sed`, `bc`).
- Assume all calculations require high precision before the final rounding to 4 decimal places.