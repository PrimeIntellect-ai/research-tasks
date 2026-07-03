You are an MLOps engineer tasked with reconstructing a data validation and inference pipeline. An old experiment's configuration was lost, but a screenshot of the pipeline's specifications was recovered and is available at `/app/experiment_notes.png`. 

The image contains crucial information regarding:
1. How to handle missing values in the dataset.
2. The exact weights and bias for a simple linear model architecture.
3. The threshold for outlier detection that determines if an entire dataset is corrupted (i.e., "evil") due to data leakage or extreme anomalies.

Your task is to write a Bash script at `/home/user/detector.sh` that acts as a binary classifier for dataset files.
- The script must take exactly one argument: the path to a CSV file.
- The CSV files have the header: `id,feature_alpha,feature_beta`.
- The script must read the CSV, apply the missing value handling strategy, compute the model inference score for each row, and check the outlier criteria.
- If the file violates the outlier criteria (meaning it is corrupted/evil), the script MUST exit with status code `1`.
- If the file is perfectly valid (clean), the script MUST exit with status code `0`.

You are restricted to standard Linux CLI tools (Bash, awk, sed, grep, etc.). Tesseract OCR is installed on the system if you need to read the image programmatically, or you can inspect it and hardcode the extracted rules into your script.

Ensure your script is executable (`chmod +x /home/user/detector.sh`). The automated verification system will test your script against a hidden corpus of clean and evil CSV files.