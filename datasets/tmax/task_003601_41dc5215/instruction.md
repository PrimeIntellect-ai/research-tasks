You are a database reliability engineer handling a critical incident. We received an automated pager alert via a voicemail, stored at `/app/alert_voicemail.wav`. This audio contains the name of a backup server that has just experienced a catastrophic storage failure.

Your task is to:
1. Transcribe the audio file to identify the exact name of the failed backup node.
2. We have a backup dependency graph stored in an SQLite database at `/home/user/backup_topology.db`. The table `backup_dependencies` has two columns: `source_node` (TEXT) and `target_node` (TEXT), indicating that `target_node` relies on the backup data from `source_node`.
3. Write a Bash script at `/home/user/impact_analysis.sh` that accepts a single argument (a node name) and outputs a strictly newline-separated list of all nodes that are directly or indirectly affected if the given node fails. The output must include the initial failed node itself, and the list must be sorted alphabetically.
4. Your Bash script must perform this graph traversal using an SQLite recursive Common Table Expression (CTE), not by iterating in Bash.

Ensure your script is executable (`chmod +x /home/user/impact_analysis.sh`). It must not print anything other than the sorted list of affected nodes (one per line) to standard output. 

Once you have written the script, run it manually with the node name you transcribed from the audio to see the impact of the current incident, and save its output to `/home/user/incident_report.txt`.