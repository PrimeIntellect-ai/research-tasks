You are an AI assistant helping a data scientist deal with a non-reproducible network optimization model.

The data scientist has a Python script `/home/user/model_fit.py` that performs gradient descent to find the optimal configuration (shortest path) of a molecular graph. Unfortunately, due to floating-point reduction order issues in the underlying library, the script produces slightly different costs and paths every time it is run.

Your task is to orchestrate an ensemble run using a Bash script to find the best configuration.

Create a Bash script at `/home/user/ensemble_run.sh` that does the following:
1. Runs `python3 /home/user/model_fit.py` exactly 25 times.
2. The Python script outputs several lines of text. You need to extract the values from the lines formatted exactly as:
   `Final Graph Cost: <cost>`
   `Optimal Network Path: <path>`
3. For each run, append a single line to `/home/user/all_runs.log` in the exact format:
   `Cost: <cost>, Path: <path>`
4. After completing all 25 runs, parse the collected data to find the run with the strictly lowest cost.
5. Write the best result to `/home/user/best_model.txt` in the following two-line format:
   Lowest Cost: <cost>
   Best Path: <path>

Finally, ensure your script has executable permissions and run it so that `/home/user/all_runs.log` and `/home/user/best_model.txt` are generated.