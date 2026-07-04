You are acting as a data science assistant for a researcher organizing and processing fragmented datasets.

I have three files located in `/home/user/data/`:
1. `metadata.csv`: Contains subject demographic data (`ID`, `Age`, `Group`).
2. `sensors.json`: Contains sensor readings for the subjects (`ID`, `Sensor_A`, `Sensor_B`).
3. `model_config.json`: Contains the weights, bias, and activation function for a pre-trained simple neural network layer.

Your task is to write and execute a Python script to process this data according to the following requirements:

1. **Multi-source joining:** Join the metadata and sensor data using the `ID` field.
2. **Schema enforcement:** Filter the joined dataset to keep only the valid rows. A row is considered valid if:
   - `ID` starts with the string "SUB".
   - `Age` is a valid integer between 18 and 100 (inclusive). If it's missing or cannot be parsed as an integer, drop the row.
   - `Sensor_A` and `Sensor_B` must be valid floating-point numbers.
3. **Model reconstruction & Inference:** Using the parameters provided in `model_config.json`, reconstruct the model logic. 
   - Compute the linear combination: `z = (Age * weight_Age) + (Sensor_A * weight_Sensor_A) + (Sensor_B * weight_Sensor_B) + bias`.
   - Apply the activation function specified in the config (e.g., if "sigmoid", apply the standard sigmoid function `1 / (1 + exp(-z))`).
4. **Output Generation:** Save the predictions for the valid rows into a CSV file at `/home/user/predictions.csv`. The file should contain exactly two columns: `ID` and `Prediction`. 
   - Round the `Prediction` values to exactly 4 decimal places.
   - The rows should be sorted alphabetically by `ID`.

Ensure your Python script cleanly handles the data loading, joining, validation, and mathematical operations. You can use standard libraries like `json`, `csv`, and `math`.