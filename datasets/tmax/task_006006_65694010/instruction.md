You are an MLOps engineer debugging a legacy inference engine written in C. The engine produces output logs tracking features, the model's prediction, and the delayed ground-truth actual state. 

We have lost the original model configuration. We know the model is a simple "decision stump" — a single node decision tree that uses exactly one feature and an integer threshold to make a binary prediction (e.g., `if feature_X > threshold, prediction = 1, else 0`).

Your task is to write a C program that processes the inference logs, reconstructs the lost model architecture (identifies the feature and the threshold), and validates the model's accuracy against the ground truth.

**Details:**
1. **Input Data**: A CSV file located at `/home/user/inference_logs.csv` with the following columns:
   `timestamp,temp_feature,pressure_feature,actual_state,predicted_state`
   - `temp_feature` and `pressure_feature` are integers.
   - `actual_state` and `predicted_state` are binary integers (`0` or `1`).

2. **Your Objective**:
   - Write a C program at `/home/user/analyze.c`.
   - The program must parse the CSV file.
   - **Model Reconstruction**: Determine which feature (`temp_feature` or `pressure_feature`) and what integer threshold was used to generate the `predicted_state`. The `predicted_state` perfectly follows the rule `if (feature > threshold) { return 1; } else { return 0; }` for exactly one of the features.
   - **Model Validation**: Calculate the validation accuracy of the model. This is the proportion of rows where `predicted_state` exactly matches `actual_state`.

3. **Output**:
   - Your C program must write a JSON file to `/home/user/analysis_result.json` containing the reconstructed model and its accuracy.
   - You do not need a JSON library; you can write the formatted string directly using standard I/O.
   - The JSON should match this exact format and spacing:
     ```json
     {
       "feature": "reconstructed_feature_name",
       "threshold": 42,
       "accuracy": 0.123
     }
     ```
   - Replace `"reconstructed_feature_name"` with either `"temp_feature"` or `"pressure_feature"`.
   - Replace `42` with the correct integer threshold.
   - Replace `0.123` with the exact validation accuracy formatted to exactly 3 decimal places.

Compile and run your C program to generate the final `analysis_result.json` file. Ensure your C code handles basic file I/O safely and uses standard libraries.