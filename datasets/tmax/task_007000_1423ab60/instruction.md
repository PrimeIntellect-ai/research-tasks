You need to create a configuration tracking system to monitor how parameters change across different deployment environments. 

Write a Python script `/home/user/config_tracker.py` that does the following:

1. **Read Configuration Files**: Read all JSON files from `/home/user/configs/`. Each file contains a flat dictionary of configuration keys and values. The filename (without `.json`) represents the environment name.
2. **Reshape Data**: Convert the data from a wide format (separate files/environments) into a long format tracking `(Key, Environment, Value)`.
3. **Aggregate Statistics**: Determine the number of total unique keys across all environments, and the number of "divergent" keys. A key is divergent if it has more than one distinct value across the environments it appears in.
4. **Template-based Generation**: Generate a Markdown report at `/home/user/summary.md` showing the divergence statistics and details. Use the following exact template structure (sort the divergent keys alphabetically in the details section, and sort the environments alphabetically for each key):
   ```
   # Configuration Divergence Report
   Total Keys: <total_keys>
   Divergent Keys: <divergent_count>

   ## Divergent Details
   - Key: <key> | Values: <env1>: <val1>, <env2>: <val2>
   ```
   *(Note: Format the Values dictionary as a comma-separated list of `env: value` pairs, sorted by environment name).*
5. **Pipeline Logging**: The script must log its progress to `/home/user/pipeline.log`. At a minimum, it must output these exact lines (the order of loaded files may vary):
   - `INFO: Loaded environment: <env_name>` (for each file)
   - `INFO: Analyzed <total_keys> total keys. Found <divergent_count> divergent keys.`
   - `INFO: Report generated at /home/user/summary.md`

You may install and use any Python libraries you need. Execute your script to produce the output files.