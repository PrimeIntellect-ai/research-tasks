You are an infrastructure engineer working on automated provisioning. We need a Python script that idempotently configures a virtual workspace for our data pipeline without requiring root access. 

Your task is to write a Python script at `/home/user/provision.py` that reads a configuration file and sets up directories, a simulated fstab file, and environment variables.

First, create the configuration file `/home/user/config.json` with the following exact content:
```json
{
  "volumes": [
    {
      "name": "raw_data",
      "source": "/home/user/storage/raw",
      "target": "/home/user/workspace/mnt/raw"
    },
    {
      "name": "processed_data",
      "source": "/home/user/storage/processed",
      "target": "/home/user/workspace/mnt/processed"
    }
  ],
  "env_vars": {
    "DATA_PIPELINE_ENV": "production",
    "WORKSPACE_ROOT": "/home/user/workspace"
  }
}
```

Next, write and execute `/home/user/provision.py` to perform the following actions idempotently (meaning the script can be run multiple times safely without duplicating entries or failing):

1. **Directory Setup**: Parse the JSON and ensure all `source` and `target` directories exist. Create them if they do not.
2. **Simulated fstab**: Generate a file at `/home/user/workspace/fstab.conf`. For each volume in the JSON, write a line in standard fstab format simulating a bind mount:
   `[source] [target] none bind 0 0`
   The lines should be sorted alphabetically by the volume `name`.
3. **Environment Setup**: Generate a shell script at `/home/user/workspace/env.sh` that exports the environment variables specified in `env_vars`. Each line should be in the format: `export KEY="VALUE"`. Sort the exports alphabetically by key.
4. **Shell Profile Configuration**: Update `/home/user/.bashrc` to source the newly created `env.sh`. You must append the exact line: 
   `source /home/user/workspace/env.sh`
   **Crucial**: This step must be idempotent. The line should only be appended if it does not already exist in `/home/user/.bashrc`.

Finally, run your script so the system is left in the provisioned state.