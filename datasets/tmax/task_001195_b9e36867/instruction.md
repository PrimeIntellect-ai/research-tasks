You are a data analyst tasked with calibrating a new set of environmental sensors. The raw data from the sensors has been dumped into a CSV file, but it contains noise, invalid readings, and system errors that need to be filtered out before you can calculate the calibration coefficients.

Your task is to build a minimal ETL pipeline, perform a linear regression, and test the numerical accuracy of the fit.

**Step 1: Data Cleaning (ETL)**
The raw data is located at `/home/user/raw_calibration.csv`. It has three columns: `x` (reference value), `y` (sensor reading), and `status`.
Create a cleaned dataset at `/home/user/clean_calibration.csv` that retains the header and only the rows meeting all the following criteria:
- `x` is greater than or equal to 0.
- `y` is a valid number (it must not be empty, `NaN`, or `null`).
- `status` is exactly `valid`.

**Step 2: Linear Regression**
Using the cleaned data, compute the Ordinary Least Squares (OLS) linear regression to find the line of best fit: $y = mx + b$, where $m$ is the slope and $b$ is the y-intercept. 

**Step 3: Numerical Accuracy Testing**
Calculate the Mean Absolute Error (MAE) of your OLS model's predictions against the actual `y` values in the cleaned dataset. 

**Output Requirement**
Generate a final report file at `/home/user/report.txt` containing exactly three lines with your computed values, rounded to exactly 4 decimal places:
Line 1: The slope ($m$)
Line 2: The y-intercept ($b$)
Line 3: The Mean Absolute Error (MAE)

You may write scripts in Python, Ruby, Perl, or use standard Linux shell utilities to complete this task.