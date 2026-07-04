You are an MLOps engineer tracking artifacts from recent experiments. 

Your automated logging system has exported 50 JSON files into the directory `/home/user/logs/`. Each JSON file represents a single training run and contains a nested structure with various metrics, including `training_time` and `val_loss`.

Your task is to:
1. Parse all the JSON files in `/home/user/logs/` to extract the `training_time` and `val_loss` for each experiment.
2. Calculate the Pearson correlation coefficient between `training_time` and `val_loss` across all 50 experiments.
3. Save this single correlation value, rounded to exactly 4 decimal places, to a file at `/home/user/correlation.txt`.
4. Generate a scatter plot of `training_time` (x-axis) vs `val_loss` (y-axis) and save it to `/home/user/scatter.png`. 

**Note on plotting:** You are operating in a headless Linux server environment without an X server. Ensure your plotting tool/script is properly configured for a headless backend so that it successfully saves a non-blank image file without crashing.

You may write your script in any language you prefer (Python, R, Ruby, etc.) and you may install any necessary packages or dependencies required for parsing, statistical analysis, and plotting.