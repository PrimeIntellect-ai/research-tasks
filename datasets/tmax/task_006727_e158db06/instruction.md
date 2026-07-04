I am building a simple ETL pipeline in Bash to evaluate a baseline linear regression model, but I suspect I'm encountering a silent data corruption issue. 

I have a dataset at `/home/user/data.csv` containing four columns: `id,f1,f2,y`.
I also have a Bash script at `/home/user/etl.sh` that processes this dataset. It calculates a prediction (`y_pred = 2.5 * f1 - 1.2 * f2`), writes the predictions to `/home/user/predictions.csv`, computes the Mean Absolute Error (MAE), and appends it to `/home/user/metrics.log`.

The problem is that my dataset has missing values (empty strings between commas, e.g., `2,,3.0,5.0`). The `awk` command in my script silently coerces these empty strings to `0` during mathematical operations, which acts as a hidden NaN-to-zero imputation. This severely skews my numerical accuracy tests!

Your task is to:
1. Fix the script `/home/user/etl.sh` so that any row with a completely empty `f1` or `f2` field is **entirely skipped** (dropped from both predictions and the MAE calculation).
2. The script must still correctly process all rows that have valid (non-empty) numbers for `f1` and `f2`.
3. The script must output the valid rows' predictions to `/home/user/predictions.csv` in the format `id,y_pred,y` (without headers).
4. The script must append the correct MAE of the valid rows to `/home/user/metrics.log` exactly in the format `MAE=<value>`.
5. Run the fixed script to generate the correct `/home/user/predictions.csv` and append the correct value to `/home/user/metrics.log`. 

Do not change the regression weights (`2.5` and `-1.2`). Make sure you run the script so the output files are generated!