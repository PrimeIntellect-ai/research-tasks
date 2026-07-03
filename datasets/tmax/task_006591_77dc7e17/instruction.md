You are a web developer working on a microservices architecture. Each microservice defines its own plugin dependencies in JSON files. We need to aggregate these dependencies into a single master configuration file, ensuring we use the highest semantic version requested across all services, and migrating the data to a new schema format.

Your task is to:
1. Write a Python script `/home/user/merge_plugins.py` that reads multiple JSON files, merges the plugin dependencies, compares semantic versions to find the highest requested version for each plugin, and outputs the result in a new schema format.
2. Write a bash script `/home/user/run_e2e.sh` that orchestrates the end-to-end process: it should run your Python script on a set of input files and generate an output file.

### Merging and Schema Rules:
Input files contain a list of objects, e.g.:
```json
[
  {"plugin": "auth", "version": "1.0.5", "enabled": false},
  {"plugin": "db", "version": "2.1.0", "enabled": true}
]
```
- **Semantic Versioning**: When the same plugin is requested by multiple files, you must keep the highest semantic version (e.g., `1.2.0` > `1.2.0-alpha.1` > `1.0.5`). You may install and use the `packaging` Python library for robust semver comparison.
- **Enabled Status**: If *any* service requests a plugin with `"enabled": true`, the final merged status for that plugin must be `active`. Otherwise, it is `inactive`.
- **New Schema**: The output JSON must be structured as follows, with plugins sorted alphabetically by name:
```json
{
  "plugins": {
    "auth": {
      "required_version": "1.2.0",
      "status": "active"
    },
    ...
  }
}
```

### Script Requirements:
- `/home/user/merge_plugins.py` must accept an output file via the `-o` or `--output` flag, and accept any number of input JSON files as positional arguments.
  Example usage: `python3 merge_plugins.py -o output.json input1.json input2.json`
- `/home/user/run_e2e.sh` must execute your Python script, reading all `.json` files in `/home/user/inputs/` and saving the output to `/home/user/final.json`. Ensure the bash script is executable.
- The input files are already provided in `/home/user/inputs/`.

Complete the task by ensuring `/home/user/final.json` is generated correctly by running your bash script.