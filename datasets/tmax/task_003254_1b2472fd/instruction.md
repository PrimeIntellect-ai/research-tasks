You are a data analyst troubleshooting a broken data pipeline. You have an incomplete and broken ETL and evaluation pipeline written in Bash at `/home/user/pipeline.sh`. 

It is supposed to process a dataset at `/home/user/data/raw_data.csv`, and run a Python evaluation script `/home/user/scripts/evaluate.py`. However, similar to a plotting script producing blank images due to a missing backend, the Python evaluation script is currently producing empty or invalid outputs because of a system misconfiguration, and the data filtering step is completely broken.

Your task is to repair and extend this Bash pipeline to perform data filtering, hyperparameter tuning, and model validation.

Perform the following steps by editing `/home/user/pipeline.sh`:
1. **Fix the ETL step**: The Bash script currently attempts to filter `raw_data.csv`. Fix it so that it extracts the header row AND all rows where the `label` column (the 4th column) is exactly `1`. Save this filtered data to `/home/user/data/filtered.csv`.
2. **Fix the configuration**: The `evaluate.py` script returns empty strings unless the environment variable `PIPELINE_MODE` is strictly set to `STRICT` in the environment before execution. Fix the Bash script to properly export this.
3. **Hyperparameter Tuning & Cross-validation**: Write a Bash loop in `pipeline.sh` that iterates over the parameter values: `0.1`, `0.5`, and `0.9`. For each value, call the evaluation script like this: 
   `python3 /home/user/scripts/evaluate.py --param <VALUE> --input /home/user/data/filtered.csv`
4. **Validation & Hypothesis Testing**: The Python script outputs a single line per run in the format:
   `SCORE: <S> CI_LOWER: <L> CI_UPPER: <U>`
   Parse these outputs in Bash. You must find the parameter that yields the highest `SCORE`, subject to the strict validation requirement that `CI_LOWER` must be strictly greater than `0.5` (i.e., we require 95% confidence that the true effect is > 0.5).
5. **Reporting**: Once the best valid parameter is identified, the Bash script must output a final report file to `/home/user/best_model.log` containing exactly one line in this format:
   `Best Param: <P>, Score: <S>, CI: [<L>, <U>]`

Run your script to ensure `/home/user/best_model.log` is generated correctly. Do not modify `evaluate.py` or `raw_data.csv`.