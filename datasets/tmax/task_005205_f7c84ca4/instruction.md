It's 3:00 AM and you've just been paged. The financial data aggregation pipeline has completely stalled out. The logs show that the script stopped producing output, and the last few times it did run successfully, the totals were off by several cents, causing major reconciliation issues downstream.

Furthermore, the original developer recently rotated the API key to read from an environment variable but forgot to save the new key to our secrets manager. Fortunately, they accidentally hardcoded the valid API key in a previous commit before replacing it with the environment variable logic.

Your tasks:
1. Navigate to the local repository at `/home/user/repo`.
2. Inspect the git history to recover the lost API key. Save this exact API key string into a new file at `/home/user/api_key.txt`.
3. Debug and fix `/home/user/repo/process_data.py`. There are two main bugs you need to resolve:
   - A bug causing the data fetching mechanism to hang indefinitely.
   - A precision loss issue in the aggregation step that causes inaccurate final totals for very large numbers. The final output must be completely exact to two decimal places.
4. Run the fixed script, ensuring you pass the recovered API key as the `API_KEY` environment variable. The script should output the final aggregated sum to `/home/user/result.txt`.

Verify your fix by checking that `/home/user/result.txt` is created and contains the correct, exact total with two decimal places.