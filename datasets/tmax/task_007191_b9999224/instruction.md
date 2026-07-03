You are acting as a data scientist working on a remote server where you only have access to standard Linux shell tools (bash, awk, sed, grep, bc, etc.). No Python, R, or compiled languages are available. 

You need to validate the analytical solutions of a set of linear models against raw observational data and calculate their Mean Squared Error (MSE) to test the numerical stability of the fits.

You have two files:
1. `/home/user/coefficients.tsv`: A tab-separated file containing the analytical model parameters for different sensors. The columns are: `SensorID`, `Slope (m)`, `Intercept (c)`. 
2. `/home/user/raw_data.log`: A poorly formatted log file containing the raw observational data. Each record is separated by a line containing only `---`. Within each record, the fields are given as `Key: Value` on separate lines. The keys are `ID` (SensorID), `X` (independent variable), and `Y` (observed dependent variable).

Your task:
1. Reshape the observational data into a tabular format.
2. For each observation, calculate the predicted value: $Y_{pred} = m \cdot X + c$.
3. Compute the squared residual: $(Y - Y_{pred})^2$.
4. Calculate the Mean Squared Error (MSE) for each SensorID.
5. Save the final results to `/home/user/model_mse.tsv`. The file should be tab-separated, with two columns: `SensorID` and `MSE`. 
6. Sort the output alphabetically by `SensorID`.
7. The MSE must be rounded to exactly 3 decimal places (e.g., `0.015`, `0.000`, `1.250`).

Example expected output format for `/home/user/model_mse.tsv`:
```
S1	0.010
S2	0.005
```

Ensure your pipeline relies exclusively on standard shell utilities.