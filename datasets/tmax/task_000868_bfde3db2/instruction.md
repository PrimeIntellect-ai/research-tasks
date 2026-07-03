You are tasked with auditing a scattered configuration directory structure for our configuration management system. 

Our systems leave behind various `.ini` configuration files across multiple nested directories. To save space and track configurations, the system uses symbolic links for unmodified base configurations, hard links for shared configuration pools, and regular files for custom overrides. 

We need you to write a script (in any language you choose) that traverses the configuration directory, parses specific data out of the files, and determines their link status, producing a final CSV report.

Here are the requirements:
1. Traverse the directory `/home/user/app_configs` recursively to find all files ending in `.ini`.
2. For each `.ini` file, determine its file link status:
   - If it is a symbolic link, classify it as `symlink`.
   - If it is not a symbolic link but has a hard link count greater than 1, classify it as `hardlink`.
   - Otherwise, classify it as `regular`.
3. Parse the contents of the `.ini` file to extract the value of the `version` key located strictly within the `[app]` section. You can assume the files are standard INI format. If a file is missing the `[app]` section or the `version` key, use the string `UNKNOWN`.
4. Generate a CSV report at `/home/user/audit_report.csv` with the following columns exactly in this order:
   `FilePath,LinkType,Version`
   - `FilePath` must be the absolute path to the `.ini` file.
   - `LinkType` must be one of `symlink`, `hardlink`, or `regular`.
   - `Version` must be the parsed version string.
5. The CSV rows must be sorted alphabetically by `FilePath`.

Please write and execute the code to generate this report. Ensure the output is strictly formatted as requested so our automated ingestion tools can process it.