You are an MLOps engineer maintaining a training pipeline. An automated experiment script at `/home/user/run_experiment.py` is failing to complete in our headless CI/CD environment because of a display backend misconfiguration.

Your task:
1. Fix `/home/user/run_experiment.py` so that it successfully generates its outputs (`results.json` and `plot.png`) without requiring a GUI or X11 display. (Hint: Look at the matplotlib backend).
2. Run the fixed script to generate the artifacts.
3. Write a bash script at `/home/user/eval.sh` that reads `results.json`, extracts the `accuracy` value, and evaluates it. 
   - If the accuracy is strictly greater than 0.80, the script should print `PASS` to standard output and exit with status code `0`.
   - If the accuracy is 0.80 or less, the script should print `FAIL` to standard output and exit with status code `1`.
   - Use standard shell utilities (like `jq`, `awk`, or `bc`) in your bash script.
   - Make sure `/home/user/eval.sh` is executable.

The final system state should have the fixed python script, the generated artifacts (`results.json` and `plot.png`), and an executable `/home/user/eval.sh` that correctly evaluates the results.