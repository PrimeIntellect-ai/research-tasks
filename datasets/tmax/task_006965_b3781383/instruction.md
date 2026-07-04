A customer has escalated an issue where their custom K-Means clustering script (`/home/user/clustering.py`) is failing. They are reporting that the script crashes with errors, fails to converge properly, and occasionally produces `NaN` or incorrect cluster centers. They suspect the input data (`/home/user/data.csv`) might contain corrupted entries due to an upstream sensor glitch that is simulating integer overflows and emitting garbage strings.

As a support engineer, your task is to diagnose and fix the script so it handles the corrupted inputs, repairs the convergence failure, and correctly computes the centroids.

Here are your specific requirements:
1. **Corrupted Input Handling:** Modify `/home/user/clustering.py` to handle any `ValueError` gracefully when parsing lines from `/home/user/data.csv`. Any line that cannot be parsed as a float should be dropped.
2. **Statistical Anomaly Investigation:** The upstream sensor issue also produces extreme numerical outliers. Filter out any successfully parsed float value `x` where `abs(x) > 1000`.
3. **Tracking Drops:** Track the 1-based line numbers of all dropped lines (both unparseable lines and numerical outliers). Write these line numbers as a comma-separated string to `/home/user/corrupted_lines.txt` (e.g., `2,5,9`).
4. **Convergence Failure Repair:** The custom `kmeans` function crashes with a `ZeroDivisionError` if a cluster becomes empty during an iteration. Fix the update step so that if a cluster is empty, it retains its centroid from the previous iteration instead of crashing.
5. **Output Centroids:** The script must output the final, converged centroids to `/home/user/centroids.txt`. The centroids must be sorted in ascending order, rounded to 2 decimal places, and comma-separated (e.g., `-5.0,11.0,102.33`).

The files `/home/user/clustering.py` and `/home/user/data.csv` have been created for you. Modify `clustering.py`, run it, and ensure both `/home/user/corrupted_lines.txt` and `/home/user/centroids.txt` are generated with the correct values.