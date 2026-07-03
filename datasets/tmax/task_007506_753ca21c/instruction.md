You are an MLOps engineer tasked with tracking experiment artifacts and finding the most similar model runs to a baseline. 

You have a directory `/home/user/experiments` containing several CSV files of training metrics.
- `baseline.csv`: The reference experiment.
- `cand_1.csv` to `cand_5.csv`: Candidate experiments.

Each file has a header `epoch,loss` and contains 100 rows of data (epochs 1 to 100).

Your task is to write a Bash script at `/home/user/analyze.sh` that performs the following:
1. Implements systematic sampling by filtering the data to only include rows where the `epoch` is an **even** number.
2. Calculates the Pearson correlation coefficient between the `loss` values of `baseline.csv` and each `cand_*.csv` file, using only the sampled (even) epochs. You must compute this using standard Unix tools (like `awk`, `paste`, `join`, etc.) directly in the bash script. Do not use Python, R, or other external programming languages.
3. Identifies the candidates and sorts them by their correlation coefficient in descending order.
4. Outputs the top 2 most positively correlated candidates to `/home/user/best_candidates.txt` in the following format:
   ```
   cand_X.csv 0.9876
   cand_Y.csv 0.8765
   ```
   The correlation values must be rounded to exactly 4 decimal places.

Run your script to generate the `/home/user/best_candidates.txt` file.

Make sure your script is executable (`chmod +x /home/user/analyze.sh`).