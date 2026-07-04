You are an MLOps engineer tasked with retrieving the most relevant and efficient model experiment from a tracking server's file dump.

You have been given two files in your home directory (`/home/user/`):
1. `artifacts.csv`: Contains metadata for recent model training runs. 
   - Format: `run_id,model_name,accuracy,loss,training_time`
   - Example: `run_1,modelA,0.95,0.05,100`
2. `embeddings.tsv`: Contains pre-computed 5-dimensional dense vector embeddings representing the textual descriptions of each run.
   - Format: `run_id|v1|v2|v3|v4|v5`
   - Example: `run_1|0.2|0.1|0.4|-0.2|0.5`

Your objective is to write a pure Bash script at `/home/user/find_best_run.sh` that performs the following steps:
1. Parse `artifacts.csv` and calculate the "efficiency score" for each run. The efficiency score is defined as `accuracy / training_time`.
2. Identify the **top 5** runs with the highest efficiency scores.
3. For only those top 5 runs, retrieve their corresponding embedding vectors from `embeddings.tsv`.
4. Calculate the dot product between each retrieved embedding and the following target query vector: `[0.1, 0.5, 0.2, -0.1, 0.8]`.
5. Identify the run (out of the top 5) that has the highest dot product with the query vector.
6. Write the result to `/home/user/best_run.txt` in the exact format: `run_id,dot_product`. Use a standard precision (e.g., standard `awk` float output).

Requirements:
- Do not use Python, R, or any other scripting language. You must rely on standard Linux utilities (e.g., `awk`, `sed`, `sort`, `join`, `grep`, `bash`).
- The script should execute successfully when run as `bash /home/user/find_best_run.sh`.