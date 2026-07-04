You are acting as a configuration manager tracking changes across heterogeneous systems. 

You have been provided with an archive of system configurations located at `/home/user/backups/configs.tar.gz`. Inside this archive, there are two configuration files exported from different legacy systems, resulting in different character encodings and structured formats:
1. `app_config.xml`: An XML file encoded in UTF-16LE.
2. `services.json`: A JSON file encoded in ISO-8859-1.

Your task is to:
1. Extract the archive into a new working directory at `/home/user/mnt/config_workspace/`.
2. Write a script (in any language you choose) to parse these files, properly handling their respective character encodings.
3. Extract the following specific configuration values:
   - From the XML file: The database `host` and `port` (located under `settings/database`).
   - From the JSON file: The cache `backend` and `port` (located under `services/cache`).
4. Output these values into a single consolidated CSV file located exactly at `/home/user/config_summary.csv`. The CSV must have the header `component,key,value`. The rows must be sorted alphabetically by `component`, then by `key`.
5. Compress the resulting CSV file into a standard zip archive located at `/home/user/config_summary.zip`. The zip archive must contain only the `config_summary.csv` file (without any directory paths).

The final state must include the `config_summary.zip` file containing the properly formatted CSV.