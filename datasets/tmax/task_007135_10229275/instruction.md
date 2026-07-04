You are a machine learning engineer preparing a dataset of sensor features for a model. The sensors suffer from a non-linear response drift. 

You have a calibration dataset at `/home/user/calibration.csv` with columns `x_true,y_obs`. The sensor observation model follows the equation:
`y_obs = A * x_true + B * (x_true ** 3)`

You also have a dataset of uncalibrated features at `/home/user/raw_features.csv` containing a single column `y_obs`.

Your task is to:
1. Perform a curve fit (regression) on `calibration.csv` to find the parameters `A` and `B` (round them to 2 decimal places for use in the next step).
2. For each `y_obs` in `raw_features.csv`, use the Newton-Raphson method to solve the non-linear equation for `x_true`.
3. Use an initial guess of `x_0 = y_obs / A`.
4. Your convergence criteria for the solver must be `abs(x_new - x_old) < 1e-5`. Keep track of the number of iterations required to converge.
5. Create a Python script at `/home/user/prepare_data.py` that implements this logic and outputs the results to `/home/user/corrected_features.csv`.
6. Run the script.

The output file `/home/user/corrected_features.csv` must be a CSV with the following header:
`y_obs,x_pred,iterations`
Where `x_pred` is the corrected feature value rounded to 4 decimal places, and `iterations` is the integer number of Newton-Raphson steps taken to reach convergence.