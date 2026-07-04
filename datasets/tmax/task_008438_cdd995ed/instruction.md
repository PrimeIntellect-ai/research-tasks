You are a Database Reliability Engineer. We have a legacy SQLite database containing our service backup metadata and dependency graph, located at `/home/user/backup_metadata.db`. Unfortunately, the original documentation for the schema has been lost.

Your task is to reverse-engineer the database schema and write a Python script that generates an automated restore pipeline for a given service.

1. Explore the SQLite database at `/home/user/backup_metadata.db` to understand the tables. It contains information about services, how they depend on each other, and logs of backup jobs.
2. Write a Python script at `/home/user/build_restore.py` that takes exactly one command-line argument: the name of a target service to restore.
    * Example usage: `python /home/user/build_restore.py PaymentGateway`
3. The script must perform the following:
    * Determine the full dependency tree for the requested service (i.e., the service itself, the services it depends on, the services those depend on, and so forth).
    * For *each* service in this dependency tree, identify the S3 URI of the **most recent successful** backup.
    * Generate a JSON file at `/home/user/restore_plan.json` containing an array of objects representing the exact sequence of backups to download and restore.
4. The JSON array must be ordered such that a dependency is always restored *before* any service that depends on it. Siblings in the dependency tree can be in any order, as long as the parent-child rule is strictly respected.
5. The format of `/home/user/restore_plan.json` must exactly match this structure:
```json
[
  {
    "service_name": "AuthService",
    "s3_uri": "s3://backups/auth/20231001.tar.gz",
    "backup_time": "2023-10-01 12:00:00"
  },
  ...
]
```

To complete the task, your final action should be running your script for the target service: `PaymentGateway`.
Ensure your script creates `/home/user/restore_plan.json` successfully with the correct data.