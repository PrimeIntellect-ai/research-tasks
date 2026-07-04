I need your help fixing and wrapping a legacy data processing component into a real-time ETL pipeline service. 

We have a legacy compiled tool located at `/app/sensor_processor` that performs anomaly and changepoint detection on sensor data. Unfortunately, the source code was lost, and the binary is stripped. We've discovered a critical bug: the tool silently drops any CSV records that contain embedded newlines inside quoted strings, which often happens in the "Sensor_Notes" field, leading to misaligned timestamps and dropped anomalies.

Your task is to build a new ETL pipeline service in C that wraps this legacy tool, fixes the data ingestion issues, and reshapes the output. 

Specifically, you must write a C program that acts as a TCP server listening on `127.0.0.1:9090`. 

**Requirements:**
1. **Authentication:** Upon connection, the client will send an auth token: `ETL_AUTH: VALID_STR_8472\n`. If the token is incorrect or missing, drop the connection immediately.
2. **Data Ingestion:** After authentication, the client will stream CSV data. The CSV has the following columns: `Timestamp (ISO8601), Sensor1_Val, Sensor2_Val, Sensor3_Val, Sensor_Notes`. Notice this is a "wide" format. The notes field may contain embedded newlines enclosed in double quotes.
3. **Extraction & Preprocessing:** Your service must correctly parse the CSV (handling the embedded newlines), extract the structured information, and strip out the newlines from the `Sensor_Notes` field so the legacy binary doesn't drop the rows.
4. **Anomaly Detection (Legacy Tool):** Pass the cleaned, newline-free CSV data to the `/app/sensor_processor` binary via standard input. The binary will output a CSV containing anomalies detected in the sequence. 
5. **Timestamp Alignment & Reshaping:** The output from the legacy tool returns anomalies in a wide format with Unix epoch timestamps. You must parse these timestamps, align them back to ISO8601, and reshape the output into a "long" format: `Timestamp (ISO8601), Sensor_ID, Anomaly_Score, Cleaned_Notes`.
6. **Output:** Send the reshaped long-format CSV data back to the TCP client, ending the stream with `EOF_PIPELINE\n`, and then close the connection.

Write the code, compile it to `/home/user/etl_server`, and leave it running in the background. Do not use external libraries other than standard POSIX C libraries.