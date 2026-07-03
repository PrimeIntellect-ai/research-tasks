You are tasked with building a C++ data pipeline for a configuration management system. We receive logs of server configuration changes, but we need to anonymize the data, extract specific numerical features, and calculate rolling statistics for monitoring purposes.

Please write a C++ program at `/home/user/process_configs.cpp` that reads an input CSV file, processes the data, and writes to an output CSV file. 

**Input Data Description:**
The input file is located at `/home/user/config_changes.csv`.
It has the following header and format:
`timestamp,user_ip,server_id,config_key,old_size_bytes,new_size_bytes`
Example row:
`1622540000,192.168.1.50,srv-01,max_connections,100,200`

**Processing Requirements:**
1. **Data Masking and Anonymization:**
   You must mask the `user_ip` field. Assuming standard IPv4 format (`X.Y.Z.W`), replace the last two octets with asterisks (`*`). 
   Example: `192.168.1.50` becomes `192.168.*.*`.

2. **Feature Extraction:**
   Calculate the `size_delta`, which is `new_size_bytes - old_size_bytes`.

3. **Rolling Statistics Computation:**
   Calculate the rolling average of the `size_delta` across the *last 3* chronological changes globally (not per server, just the sequence of rows in the file). 
   - If there is only 1 record so far, the average is just its delta.
   - If there are 2 records, it's the average of those 2.
   - For 3 or more records, it's the average of the current record and the previous 2 records.
   Output this average formatted exactly to 2 decimal places (e.g., `100.00`).

**Output Data Description:**
Your C++ program should write the processed data to `/home/user/processed_changes.csv`.
The output CSV must have the following header:
`timestamp,masked_ip,server_id,config_key,size_delta,rolling_avg_delta`
Example corresponding output row:
`1622540000,192.168.*.*,srv-01,max_connections,100,100.00`

**Execution:**
You should compile your program using:
`g++ -O3 -std=c++17 /home/user/process_configs.cpp -o /home/user/process_configs`
And then run it to generate the `/home/user/processed_changes.csv` file. Ensure the C++ program safely handles potential empty lines at the end of the input file.