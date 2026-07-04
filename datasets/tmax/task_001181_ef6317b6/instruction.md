You are an infrastructure engineer automating a staged deployment system. You need to write a Python script that performs a rolling update of configuration files across multiple application instances, with built-in backup, validation, and automated rollback capabilities.

Your task is to write and execute a Python script at `/home/user/deploy.py` that implements this deployment strategy. 

### Environment Setup
There are 5 application instances located in `/home/user/instances/`. They are named `inst1`, `inst2`, `inst3`, `inst4`, and `inst5`.
Inside each instance directory, there is a configuration file named `config.json`.
Currently, every `config.json` contains:
```json
{"version": "1.0", "theme": "blue"}
```

There is an existing validation script at `/home/user/validate.py`. You can run it against an instance directory like this:
`python3 /home/user/validate.py /home/user/instances/inst1`
It will exit with code `0` if the instance configuration is valid, and code `1` if it is invalid.

### Deployment Requirements
Write `/home/user/deploy.py` to do the following:

1. **Target Configuration**: You are deploying a new configuration. The new state for `config.json` in every instance should be:
   ```json
   {"version": "2.0", "theme": "green"}
   ```

2. **Staged Rollout**: Process the instances in batches. The batch size should be 2.
   - Batch 1: `inst1`, `inst2`
   - Batch 2: `inst3`, `inst4`
   - Batch 3: `inst5`
   
   Wait 1 second between processing each batch.

3. **Backup Strategy**: Before modifying an instance's configuration, copy its current `config.json` to `/home/user/backups/` with the name `<instance_name>_config.json.bak` (e.g., `inst1_config.json.bak`). Create the `backups` directory if it doesn't exist.

4. **Validation and Rollback**: After a batch is fully updated (both configurations rewritten), run `/home/user/validate.py` on each instance in that batch.
   - If *all* instances in the batch pass validation (exit code 0), proceed to the next batch.
   - If *any* instance in the batch fails validation (exit code 1), you must **abort the deployment and rollback**.
   - A rollback means restoring the `config.json` from the backup for *every instance that has been modified so far*, across all past and current batches. Do not restore instances that haven't been touched yet.

5. **Logging**: Your script must append its actions to `/home/user/deploy.log` in the exact format shown below.
   For each action, write one line:
   - When backing up: `INFO: Backup <inst>`
   - When updating: `INFO: Update <inst>`
   - When validation succeeds: `INFO: Validate <inst> - SUCCESS`
   - When validation fails: `ERROR: Validate <inst> - FAILED`
   - When rolling back an instance: `INFO: Rollback <inst>`
   - When rollback of all affected instances is complete: `CRITICAL: Rollback complete`
   - If the entire deployment finishes successfully: `SUCCESS: Deployment complete`

   *Note on Rollback order:* Rollback must happen in the reverse order of updates (e.g., if inst1, inst2, inst3, inst4 were updated, rollback inst4, then inst3, then inst2, then inst1).

### Execution
Once you have written `/home/user/deploy.py`, run it. One of the instances has been intentionally rigged to fail validation with the new configuration. Ensure your script correctly identifies the failure, executes the full rollback, logs the events properly, and exits.