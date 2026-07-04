You are tasked with fixing and enhancing a data processing pipeline for a configuration management system.

We have a raw CSV file at `/home/user/raw_audit.csv` that contains configuration change logs. The columns are `Timestamp,Author,ConfigValue`.
Currently, the pipeline drops or corruptes rows that contain embedded newlines within the `ConfigValue` field (which are enclosed in double quotes). 
Additionally, we need to anonymize the data by masking any IPv4 addresses in the `ConfigValue` field.

Your task is to write a C++ program at `/home/user/process.cpp` (you can start from scratch or use any standard C++17 features) that:
1. Reads `/home/user/raw_audit.csv`.
2. Properly parses the CSV, strictly respecting double quotes `"` for fields that contain embedded newlines, commas, or escaped double quotes `""`.
3. Anonymizes any IPv4 address (e.g., `192.168.1.1`) found in the `ConfigValue` column by replacing it entirely with the string `[REDACTED]`. An IPv4 address is defined as four groups of 1 to 3 digits separated by periods.
4. Writes the processed records to `/home/user/clean_audit.csv`. The output must remain a valid CSV. The `ConfigValue` column in the output must be enclosed in double quotes. `Timestamp` and `Author` do not need quotes.

Compile your program using `g++ -O3 -std=c++17 /home/user/process.cpp -o /home/user/process` and run it so that `/home/user/clean_audit.csv` is generated.

Do not use external non-standard C++ libraries (like Boost) for this task; rely on the standard library.