You are a Cloud Architect orchestrating the migration of legacy services to a new cloud infrastructure. You need to write and execute a Bash deployment script that sets up the environments and configurations for these migrated services on a staging server.

Write a Bash script at `/home/user/deploy_migration.sh` and run it. The script must perform the following tasks based on a mapping file provided at `/home/user/legacy_topology.csv`.

**Input File: `/home/user/legacy_topology.csv`**
This file (which already exists) has the following CSV format:
`ServiceName,LegacyIP,LegacyPort,CloudDBHost,NewPort,TargetGroup`
*(The first line is a header: `ServiceName,LegacyIP,LegacyPort,CloudDBHost,NewPort,TargetGroup`)*

**Your script must do the following for each service listed in the CSV (skipping the header):**

1. **Environment & Profile Setup:**
   - Create a service directory at `/home/user/services/<ServiceName>`
   - Inside this directory, create a shell profile file named `.app_profile`
   - The `.app_profile` must contain the following exactly (with `<...>` replaced by actual values from the CSV):
     ```bash
     export APP_ENV="cloud_migration"
     export CLOUD_DB_HOST="<CloudDBHost>"
     export APP_PORT="<NewPort>"
     export MIGRATION_STATUS="ACTIVE"
     ```

2. **System Config File Management:**
   - Ensure the directory `/home/user/system_configs` exists.
   - For each service, generate a configuration file at `/home/user/system_configs/<ServiceName>_proxy.conf`
   - The contents of this config file must be exactly:
     ```ini
     [ProxyConfig]
     ListenPort=<NewPort>
     Upstream=<LegacyIP>:<LegacyPort>
     RequireGroup=<TargetGroup>
     ```

3. **Migration Reporting:**
   - After processing all services, the script must generate a final report at `/home/user/migration_report.json`
   - The JSON file must have the following exact structure, with services sorted alphabetically by `ServiceName`:
     ```json
     {
       "migrated_services": [
         {
           "name": "<ServiceName>",
           "port": <NewPort>,
           "profile_path": "/home/user/services/<ServiceName>/.app_profile"
         },
         ...
       ],
       "total_services": <Number of services processed>
     }
     ```

**Constraints & Rules:**
- Do not use any elevated privileges (`sudo` or `su`).
- Ensure the script is executable (`chmod +x`) before running it.
- Your script must parse the CSV using standard Bash tools (e.g., `awk`, `sed`, or a `while read` loop).
- Make sure to handle potential carriage returns or whitespace correctly.
- Execute the script so the final state is present on the system.