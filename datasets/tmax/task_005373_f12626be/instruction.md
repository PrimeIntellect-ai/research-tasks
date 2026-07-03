A researcher left behind a broken data analysis pipeline in `/home/user/workspace`. The pipeline is supposed to merge two sensor datasets, clean the data, train a regression model, and plot the results. However, the script crashes, fails to handle missing values, and the researcher mentioned that "the plot never saves properly on the headless server, it just hangs or produces a blank file."

Your task is to fix and run the Python script `/home/user/workspace/analysis.py` to meet the following exact specifications:

1. **Multi-source data joining**: The script must read `/home/user/workspace/sensor_A.csv` and `/home/user/workspace/sensor_B.csv` and perform an inner join on the `id` column.
2. **Missing value handling**: Fill any missing values in the `humidity` column with the median of the available `humidity` values in the merged dataset.
3. **Outlier handling**: Remove any rows where the `temp` value is strictly greater than 50 (these are sensor malfunctions).
4. **Regression**: Train a `sklearn.linear_model.LinearRegression` model to predict `temp` using `pressure` and `humidity` as features (in that exact order).
5. **Outputs**:
   - Save the model's parameters to `/home/user/workspace/model_results.json`. The JSON must have exactly these keys: `"pressure_coef"`, `"humidity_coef"`, and `"intercept"`. Round the values to 4 decimal places.
   - Fix the plotting issue so that the script successfully generates a scatter plot of True vs Predicted temperatures and saves it to `/home/user/workspace/predictions.png`. Ensure it works in a headless Linux environment.

Modify the script as needed and execute it to generate the output files.