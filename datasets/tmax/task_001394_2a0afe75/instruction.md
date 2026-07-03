You are assisting a researcher who is trying to extract datasets from a misconfigured, live sensor array system. 

The system consists of three local services that are supposed to work together, but are currently disconnected or misconfigured:
1. **Sensor Log Generator**: A background process that continuously generates multi-line XML sensor readings and writes them to `/home/user/data/active.log`. Due to legacy hardware, some readings are encoded in UTF-8, while others are in ISO-8859-1.
2. **Aggressive Archiver**: A background script that hastily rotates `active.log` into the `/home/user/data/archives/` directory every few seconds, compressing them to `.gz`. Because it races with the generator, some `.gz` files end up with incomplete/truncated gzip trailers.
3. **Analytics API**: A local web server running on `http://127.0.0.1:8080`. It has an endpoint `POST /submit` that accepts JSON payloads representing parsed sensor readings.

Your tasks:
1. Review the service startup script located at `/app/services/start_all.sh` and fix any configuration mismatches (e.g., port bindings, directory paths) so the services can communicate locally. Start the services and let them run for at least 15 seconds to accumulate data.
2. Write a Go program at `/home/user/parser.go` that:
   - Scans `/home/user/data/archives/` for all `.gz` archive files.
   - Robustly reads each archive. It MUST handle trailing garbage or incomplete gzip streams without crashing (recovering all valid lines up to the corruption point).
   - Parses the multi-line XML log records. A record starts with `<Reading>` and ends with `</Reading>`.
   - Handles the mixed character encodings (UTF-8 and ISO-8859-1) so that text fields are properly decoded to standard UTF-8 strings.
   - Extracts the `SensorID`, `Value` (as a float64), and `Timestamp`.
   - Discards any readings where `Value` is less than `0.0`.
   - Streams the parsed, valid readings as JSON objects to the Analytics API (`POST http://127.0.0.1:8080/submit`). The API expects the payload format: `{"sensor_id": "...", "value": 12.34, "timestamp": "..."}`.

**Verification:**
Once your Go program finishes executing, our automated test will query the Analytics API's internal metrics. The test will calculate the **Recovery Recall** (the number of valid, correctly parsed records received by the API divided by the known total number of valid records generated). 
You must achieve a Recovery Recall of **>= 0.98** (98%) within a runtime of **< 5 seconds** for your Go program execution.

Do not stop the services once started; the verification script will evaluate the system while the API is live.