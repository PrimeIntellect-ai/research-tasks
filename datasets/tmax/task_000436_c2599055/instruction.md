You are tasked with building a configuration tracking tool. As a configuration manager, you have inherited a legacy system that backs up server configurations into a custom archive format called `.ccp` (Custom Config Pack).

There is a master archive located at `/home/user/config_backups.ccp`. 
Despite the custom extension, this master file is actually a standard gzip-compressed tarball (`.tar.gz`).

Inside this master archive, you will find:
1. An `index.xml` file.
2. Several nested archives (a mix of `.zip` and `.tar.gz` files) representing different configuration versions.

The `index.xml` file has the following structure:
```xml
<backups>
    <version id="v1" file="backup_v1.zip" date="2023-10-01" />
    <version id="v2" file="backup_v2.tar.gz" date="2023-10-02" />
    <version id="v3" file="backup_v3.zip" date="2023-10-03" />
</backups>
```

Inside *each* nested archive, there are two files you care about:
1. `app_config.json`: Contains nested JSON data. You need to extract the integer value at the JSON path `database.max_connections`.
2. `services.csv`: A CSV file with headers `service_name,port,status`. You need to extract the integer `port` for the row where `service_name` is exactly `cache_service`.

Your task:
Write a Python script at `/home/user/config_tracker.py` that processes the `/home/user/config_backups.ccp` archive, extracts the nested archives, parses the structured files, and tracks the changes to these two specific configuration values across the versions defined in `index.xml`.

Run your script to generate a final report at `/home/user/change_report.json`. The output must be a valid JSON file mapping the version IDs from the XML to their respective extracted values, strictly matching this schema:
```json
{
  "v1": {
    "max_connections": 100,
    "cache_port": 6379
  },
  "v2": {
    "max_connections": 150,
    "cache_port": 6380
  }
}
```
(Note: the actual version IDs and values will depend on the archive contents).

You may install any standard Python packages using `pip` if needed, though standard library modules like `tarfile`, `zipfile`, `json`, `xml.etree.ElementTree`, and `csv` should be sufficient. Do not hardcode the expected output; your script must dynamically read the archive.