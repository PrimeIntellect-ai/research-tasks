You are a data engineer building an automated data quality and modeling pipeline for incoming IoT sensor data. You have been provided with a CSV file at `/home/user/sensor_data.csv`.

Your objective is to write and execute a script (in the language of your choice) that performs the following pipeline steps:

1. **Correlation Analysis & Feature Selection:**
   - Read the dataset `/home/user/sensor_data.csv`. The dataset contains a `timestamp` column, a `target_temp` column, and several sensor feature columns (`sensor_A`, `sensor_B`, `sensor_C`, `sensor_D`).
   - Calculate the Pearson correlation matrix for the sensor feature columns only (ignore `timestamp` and `target_temp`).
   - Identify any pairs of sensors that have an absolute correlation strictly greater than `0.90`.
   - For each highly correlated pair, you must drop one of the sensors to reduce redundancy. Always drop the sensor whose name comes **later** in alphabetical order (e.g., if `sensor_X` and `sensor_Y` are highly correlated, drop `sensor_Y`). 

2. **Model Training and Evaluation:**
   - Using only the retained sensor columns as features, train a standard ordinary Linear Regression model to predict the `target_temp`.
   - Before training, split the dataset into training and testing sets based on time/index order: the first 80% of the rows must be the training set, and the remaining 20% must be the testing set. **Do not shuffle the data.**
   - Calculate the Root Mean Squared Error (RMSE) of your model's predictions on the testing set.

3. **Reporting:**
   - Output your results to a JSON file located at `/home/user/report.json`.
   - The JSON file must have exactly the following structure and keys:
     ```json
     {
       "dropped_sensors": ["list", "of", "dropped", "sensor", "names", "alphabetically", "sorted"],
       "retained_sensors": ["list", "of", "retained", "sensor", "names", "alphabetically", "sorted"],
       "rmse": 1.23
     }
     ```
   - The `rmse` value should be a number rounded to exactly 2 decimal places.

You are responsible for setting up your environment (e.g., installing necessary libraries like pandas, scikit-learn, etc., if using Python). Ensure that the final `/home/user/report.json` file is correctly formatted and contains the accurate values derived from the dataset.