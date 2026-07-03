You are acting as a configuration manager for a legacy application. The system receives configuration updates in JSON format, but the legacy backend requires them in CSV format. You need to process a new incoming configuration update.

Here is your task:
1. Locate the incoming JSON configuration file at `/home/user/app_config/incoming/v2_update.json`.
2. Parse this JSON file. Convert its key-value pairs into a CSV format where the first column is the key and the second column is the value (e.g., `key,value`). 
3. Sort the CSV rows alphabetically by the key. Do not include a header row.
4. Save the resulting CSV file to `/home/user/app_config/history/v2_update.csv`.
5. The application always looks for its current configuration via a symbolic link. Create a symbolic link at `/home/user/app_config/active/current.csv` that points to the absolute path of the newly created CSV file (`/home/user/app_config/history/v2_update.csv`).
6. Finally, create an XML log file at `/home/user/app_config/deploy_log.xml` to track this change. The XML must have the following exact structure and values:
```xml
<deployment>
  <version>v2_update</version>
  <keys>[NUMBER_OF_KEYS]</keys>
</deployment>
```
Replace `[NUMBER_OF_KEYS]` with the integer number of keys present in the JSON configuration.

You may use any standard Linux tools or write a script in Python/Bash to accomplish this.