You are acting as a cloud architect migrating legacy worker services to a new environment using a staged rolling deployment. 

Our operations team uses an old interactive Python tool located at `/home/user/legacy_deploy.py` to manage the lifecycle of these services. Currently, deploying a service requires manually answering several interactive prompts. 

Your task is to fully automate this staged deployment process. Write a Python script at `/home/user/auto_migrate.py` that uses the `pexpect` module to programmatically interact with `/home/user/legacy_deploy.py`.

Your script must perform a rolling deployment by sequentially migrating three services: `worker-1`, `worker-2`, and `worker-3`. 

For each service, you must execute `/home/user/legacy_deploy.py` and handle the following exact interactive prompts:
1. `Enter service name to migrate: ` -> You should provide the service name (e.g., `worker-1`).
2. `Enter target version: ` -> You should provide `v2.1`.
3. `Verify pre-checks passed? (yes/no): ` -> You should provide `yes`.
4. `Bring service online? (y/n): ` -> You should provide `y`.

Write `/home/user/auto_migrate.py`, ensure it is executable, and then run it so that all three services are successfully migrated. The `legacy_deploy.py` script automatically records successful migrations in `/home/user/migration_log.json`. Ensure your script runs to completion and that the log file correctly reflects all three services upgraded to `v2.1` and online.