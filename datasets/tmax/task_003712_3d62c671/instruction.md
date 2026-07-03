We are migrating our telemetry data processing pipeline. Our upstream systems send raw CSV data containing wide-format sensor readings via HTTP, but due to legacy data corruption, some rows contain embedded newlines inside quoted fields.

You need to build a C-based ETL web service that processes this data, leverages a legacy anomaly detection binary, and returns a templated alert report.

Here are your requirements:
1. Write a C program that listens for HTTP POST requests on `0.0.0.0:9000` at the endpoint `/process`.
2. The HTTP request body will be a CSV with the header: `timestamp,sensor1,sensor2,sensor3`.
3. **Data Cleaning:** You must silently *drop* any CSV row that contains an embedded newline (i.e., a newline character inside a quoted field).
4. **Reshaping:** Reshape the remaining wide-format rows into long format: `timestamp,sensor_name,value`.
5. **Anomaly Detection:** We have provided a legacy stripped binary at `/app/legacy_scorer`. You must pass the long-format data (excluding headers) to its standard input. It expects lines formatted as `timestamp,sensor_name,value` and will output `timestamp,sensor_name,score`.
6. **Reporting:** For every row where the output `score` from the legacy binary is `1`, generate a text alert using this exact template: `ALARM: Sensor {sensor_name} at {timestamp} triggered an anomaly!\n`
7. The HTTP response must be `200 OK` with `Content-Type: text/plain` and the body containing the concatenated alert lines in the order they were processed.

Ensure your C server is robust enough to handle standard HTTP POST requests and runs continuously. You may use standard POSIX C libraries. Compile your code to `/home/user/etl_server` and run it in the background.

To test your binary, the verification system will send HTTP POST requests to `http://127.0.0.1:9000/process` with various CSV payloads and assert the response body.