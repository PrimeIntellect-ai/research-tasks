You are an AI assistant tasked with building a configuration manager change tracking pipeline. We have a set of server metadata and a log of configuration changes. You need to write a C++ program and a bash orchestrator to join these datasets, anonymize sensitive information, and generate region-specific configuration change reports based on a strict template.

### Input Data
You will find two files in `/home/user/`:
1. `/home/user/servers.csv` - Contains server metadata.
   Format: `ServerID,Region,IPAddress,OwnerEmail`
2. `/home/user/changes.csv` - Contains historical configuration changes.
   Format: `ServerID,Timestamp,UserID,ConfigKey,NewValue`

### Requirements

1. **C++ Processing Program (`/home/user/process_configs.cpp`)**
   Write a C++ program (compileable with `g++ -std=c++17`) that reads both CSV files and joins them on `ServerID`.
   For each matched change record, you must apply the following masking rules to the sensitive data:
   * **IPAddress**: Replace the last octet (everything after the last `.`) with `XXX`. (e.g., `10.0.0.15` -> `10.0.0.XXX`)
   * **OwnerEmail**: Keep the first 2 characters of the local part, replace the rest of the local part with `***`, and keep the `@domain` intact. (e.g., `admin1@company.com` -> `ad***@company.com`)
   * **UserID**: Keep the first character and the last character, and put `***` between them. (e.g., `U98765` -> `U***5`)

   Using the masked data, generate formatted text entries using the exact template below:
   ```
   Server: <ServerID>
   IP: <MaskedIP>
   Admin: <MaskedEmail>
   Changed <ConfigKey> to <NewValue> by <MaskedUserID> at <Timestamp>
   ---
   ```

   The C++ program should write these formatted records into region-specific text files inside `/home/user/reports/`. The filename must be `region_<Region>.txt` (e.g., `region_US-East.txt`). Records in each file should be appended in the order they appear in `changes.csv`.

2. **Pipeline Orchestrator (`/home/user/run_pipeline.sh`)**
   Write a bash script that:
   * Creates the `/home/user/reports/` directory if it doesn't exist, or clears its contents if it does.
   * Compiles your C++ program to `/home/user/process_configs`.
   * Executes the C++ program.

Ensure your bash script has execute permissions and runs successfully without errors.