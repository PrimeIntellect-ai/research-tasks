You are an operations engineer triaging a recurring issue in our metrics processing pipeline. 

We have a Python script located at `/home/user/metric_app/process_metrics.py` that processes a batch of JSON metrics from `/home/user/metric_app/metrics.json`. However, the pipeline fails intermittently. We've traced it down to a specific data edge-case causing a crash during the variance calculation. 

Additionally, the script requires an authorization token to export the results. The token was accidentally committed to the git repository a few days ago and then removed, so we no longer have it in our environment.

Your objectives:
1. **Recover the secret token**: Inspect the git history in `/home/user/metric_app` to find the leaked authorization token. Write this exact token string to a new file at `/home/user/metric_app/recovered_token.txt`.
2. **Fix the algorithmic bug**: Identify the intermittent failure in `/home/user/metric_app/process_metrics.py`. The error occurs when calculating the variance of a metric array. Update the `calc_variance` function so that if the array contains exactly 1 element, it returns `0.0` instead of crashing.
3. **Execute the pipeline**: Run the script using the recovered token as an environment variable to generate the final output. The command should look like this:
   `cd /home/user/metric_app && TOKEN=$(cat recovered_token.txt) python process_metrics.py`

If successful, the script will process all records without crashing and output the calculated variances to `/home/user/metric_app/output.txt`. 

Please complete these steps. The automated test will verify the contents of `/home/user/metric_app/recovered_token.txt` and `/home/user/metric_app/output.txt`.