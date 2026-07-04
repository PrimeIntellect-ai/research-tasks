You are a Database Reliability Engineer investigating a set of backup system metric databases. The original documentation is lost, and you only have access to two SQLite database files left behind by the previous engineer: `/home/user/db_backups/primary_metrics.db` and `/home/user/db_backups/topology.db`.

Your task is to:
1. Explore these databases and reverse-engineer their schemas. One contains host information and backup job metrics, while the other contains a directed graph of replication links between hosts.
2. Write a Python script at `/home/user/generate_report.py` that takes three command-line arguments: `--region`, `--bad-state`, and `--min-downstream`.
3. The script must execute a single SQLite operation (by using SQLite's `ATTACH DATABASE` feature) to cross-query both databases. Use parameterized queries for the inputs.
4. The query should identify all hosts in the specified `--region` that:
   - Have at least one backup job in the state specified by `--bad-state`.
   - Act as a source replication node to at least the number of distinct destination hosts specified by `--min-downstream`.
5. For these identified vulnerable hosts, calculate the total size (in MB) of all their backups that are in the 'SUCCESS' state.
6. The script must output the results to `/home/user/report.json` as a JSON array of objects, sorted by `host_id` ascending.

Format of `/home/user/report.json`:
```json
[
  {
    "host_id": 101,
    "host_name": "db-node-01",
    "total_success_mb": 4500
  }
]
```

To complete the task, manually run your script like this:
`python3 /home/user/generate_report.py --region "EU-Central" --bad-state "CORRUPT" --min-downstream 2`

Ensure that your script generates the `report.json` file perfectly matching the requested format.