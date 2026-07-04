You are tasked with building a lightweight data processing and inference pipeline using only Bash and standard GNU utilities (like `awk`, `sed`, `grep`). As a data scientist, you sometimes need to clean datasets and run simple heuristic models directly in the shell before moving to heavier tools.

You are provided with a raw dataset of user profiles at `/home/user/raw_data.csv`. The file has a header and the following columns: `user_id,age,income,score1,score2`.

Your objective is to write a Bash script at `/home/user/pipeline.sh` that reads this file and performs the following data cleaning, regression inference, and similarity search steps:

1. **Missing Value & Outlier Handling:**
   - If `age` is missing (empty string), impute it with the default value of `35`.
   - If `income` is negative, clip it to `0`.

2. **Model Inference (Regression):**
   - Apply a pre-trained linear regression model to predict Customer Lifetime Value (LTV).
   - The formula is: `predicted_LTV = (0.5 * age) + (0.01 * income) + (2.0 * score1) - (1.5 * score2) + 10`
   - Calculate this value for all users after the cleaning step.

3. **Output Predictions:**
   - Save the predictions to `/home/user/cleaned_predictions.csv`.
   - The file should have the header `user_id,predicted_LTV`.
   - Format `predicted_LTV` to exactly 2 decimal places.

4. **Similarity Search:**
   - We want to find the user who is most similar to user `U001` based *only* on the Euclidean distance of `score1` and `score2`.
   - Calculate the distance between `U001` and all other users.
   - Output *only* the `user_id` of the closest user (excluding `U001` themselves) to the file `/home/user/nearest_to_U001.txt`.

Ensure your script `/home/user/pipeline.sh` is executable and can be run without any arguments to produce the required output files. Use standard command-line tools available in a standard Linux environment. Do not use Python, R, or any external data science libraries; rely entirely on Bash tools like `awk`.