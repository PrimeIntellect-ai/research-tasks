You are an AI assistant helping a researcher organize their dataset and perform some mathematical modeling and experiment tracking.

The researcher has a set of 2D sensor readings saved in a CSV file located at `/home/user/sensor_data.csv`. The file has a header `x,y` and contains floating-point values.

Your task is to set up a small analysis pipeline by writing a C program to train a simple linear regression model on this data, evaluate it, and track the experiment by outputting a JSON log.

Please perform the following steps:

1. **Model Implementation (C)**:
   Write a C program at `/home/user/linear_regression.c`. This program must:
   - Read `/home/user/sensor_data.csv`, skipping the header line.
   - Compute the line of best fit $y = mx + c$ using Ordinary Least Squares (Simple Linear Regression), where $m$ is the slope and $c$ is the intercept.
   - Compute the Mean Squared Error (MSE) of the predictions over the training set.
   - Print the results to standard output in exactly this format (floating point numbers to 4 decimal places):
     ```
     Slope: <value>
     Intercept: <value>
     MSE: <value>
     ```

2. **Experiment Tracking Pipeline**:
   Write a bash script at `/home/user/evaluate.sh`. This script must:
   - Compile `/home/user/linear_regression.c` to an executable named `/home/user/lr_model` (include the math library if necessary).
   - Execute the compiled program.
   - Parse the output and construct a JSON file located at `/home/user/model_metrics.json`.
   - The JSON file must have exactly the following structure (with the computed values formatted to 4 decimal places):
     ```json
     {
       "model": "linear_regression",
       "parameters": {
         "slope": <m_value>,
         "intercept": <c_value>
       },
       "evaluation": {
         "mse": <mse_value>
       }
     }
     ```

Ensure the bash script is executable. You can assume standard utilities (`gcc`, `awk`, `sed`, `jq`, etc.) are available. Do not use external libraries for the C code besides the standard C library (`stdio.h`, `stdlib.h`, `math.h`, `string.h`).