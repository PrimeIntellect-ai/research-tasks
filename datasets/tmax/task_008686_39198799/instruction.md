You are a cloud architect migrating a legacy on-premise service to a new cloud environment. As part of the CI/CD pipeline for this migration, you need to write an idempotent Python script that processes a legacy user export, provisions the new application's directory structure, sets appropriate file permissions, and generates a Role-Based Access Control (RBAC) configuration.

A legacy export file exists at `/home/user/legacy_users.csv` with the following header and format:
`username,department,role`

Your task is to create a Python script at `/home/user/migrate_pipeline.py` that accomplishes the following:

1. **CLI Arguments**: The script must accept a single argument `--env` which can be either `staging` or `prod`.
2. **Idempotent Directory Creation**: 
   - The script must create a base deployment directory at `/home/user/cloud_deployment/<env>/`. 
   - If the directory already exists, it should be cleared/recreated to ensure a clean state (idempotency).
3. **Application Structure & Permissions**:
   - Read the `/home/user/legacy_users.csv` file.
   - For every unique `department` found in the CSV, create a subdirectory: `/home/user/cloud_deployment/<env>/<department>/`.
   - Set the permissions of each department directory to `755`.
   - Inside each department directory, create two empty files: `__init__.py` and `settings.conf`. Set the permissions of these files to `644`.
4. **RBAC Configuration (User Administration)**:
   - Generate an RBAC configuration file at `/home/user/cloud_deployment/<env>/rbac.json`.
   - The JSON file must group all users by their `role`. The structure should be a dictionary where the keys are the role names, and the values are alphabetically sorted lists of usernames that have that role. 
   - Example format: `{"admin": ["alice", "bob"], "viewer": ["charlie"]}`.
   - The JSON must be pretty-printed with an indentation of 4 spaces.
5. **CI/CD Logging**:
   - The script must generate a log file at `/home/user/migration_summary_<env>.log`.
   - The file must contain exactly one line with the following format:
     `[<env>] Deployment ready. Migrated <X> users across <Y> departments.`
     *(Where `<X>` is the total number of users parsed, and `<Y>` is the total number of unique departments).*

Once you have written the script, execute it twice in your terminal:
1. `python3 /home/user/migrate_pipeline.py --env staging`
2. `python3 /home/user/migrate_pipeline.py --env prod`

Ensure your script handles standard modules only (e.g., `os`, `sys`, `csv`, `json`, `shutil`, `argparse`).