You are an MLOps engineer tasked with building a lightweight Bash-based ETL pipeline to process and track experiment artifacts. We have a set of experiment logs in JSON format, and we need to extract both numerical metrics and text-based notes to generate a consolidated tracking summary.

Your task is to write a Bash script at `/home/user/process_artifacts.sh` that processes all JSON files located in `/home/user/experiments/`. 

The pipeline must perform the following steps:
1. **Data Extraction & Tokenization**: 
   - Parse the `notes` field from each JSON file.
   - Convert the text to lowercase.
   - Strip out all characters except letters (`a-z`) and spaces.
   - Tokenize the text into individual words.
   - Count the total frequency of each word across all experiment logs.
   - Determine the top 3 most frequent tokens.

2. **Numerical Aggregation**:
   - Parse the `accuracy` and `loss` values from the `metrics` object in each JSON file.
   - Calculate the **mean accuracy** across all experiments, rounded to two decimal places.
   - Calculate the **maximum loss** across all experiments, formatted to two decimal places.

3. **Report Generation**:
   - The script must generate a final summary report saved to `/home/user/summary.json`.
   - The output must strictly follow this JSON structure:
     ```json
     {
       "mean_accuracy": 0.00,
       "max_loss": 0.00,
       "top_tokens": [
         {"token": "word1", "count": 10},
         {"token": "word2", "count": 8},
         {"token": "word3", "count": 5}
       ]
     }
     ```
   - Ensure the `top_tokens` array is sorted in descending order of frequency. (If there is a tie, any order for the tied tokens is acceptable, but the provided dataset will have a clear top 3).

Ensure your script is executable and runs successfully without root privileges. You may use standard Linux utilities like `jq`, `awk`, `sed`, `grep`, and `bc` which are pre-installed in the environment. Run your script to generate the final `/home/user/summary.json` file.