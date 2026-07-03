You are a Database Reliability Engineer. We have experienced a backup system failure where several concurrent backup transactions deadlocked and corrupted certain backup snapshots. 

We represent our backup lineage as a directed graph in a CSV edge list. You need to analyze this dependency graph using standard shell utilities to find the most critical healthy backups to prioritize for replication.

Files provided to you:
1. `/home/user/backup_deps.csv`: A CSV file containing backup dependencies. Format: `dependent_backup_id,base_backup_id`. This means `dependent_backup_id` requires `base_backup_id` to be restored.
2. `/home/user/corrupted.txt`: A plain text file containing a list of corrupted backup IDs (one per line).

Your task:
1. Filter the dependency graph to exclude any edges where either the `dependent_backup_id` OR the `base_backup_id` is present in the `corrupted.txt` list.
2. For the remaining healthy graph, calculate the out-degree (the number of dependents) for each `base_backup_id`.
3. Find the top 3 most critical backups (those with the highest number of dependents). If there is a tie in the number of dependents, break the tie by sorting the `backup_id` in ascending lexicographical order.
4. Export the top 3 results into a JSON array in exactly this format:
   ```json
   [
     {"backup_id": "ID1", "deps": X},
     {"backup_id": "ID2", "deps": Y},
     {"backup_id": "ID3", "deps": Z}
   ]
   ```
5. Save this JSON output to `/home/user/top_backups.json`.

Ensure your final JSON file is strictly valid JSON, containing only the array and no additional text. Do not install any external tools; use standard bash, awk, grep, sort, etc.