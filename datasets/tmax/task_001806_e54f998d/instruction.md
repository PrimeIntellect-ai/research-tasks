You are an operations engineer triaging a production incident. We have a legacy C-based HTTP service located at `/app/server.c` that processes telemetry data from our hardware devices. Recently, the service has been crashing intermittently when processing data from our newest batch of devices. 

Your tasks are to:
1. **Extract Configuration:** We have an image of the new device's factory label at `/app/device_label.png`. Use `tesseract` to extract the `DEVICE_SN` and `MAGIC_KEY` values from this image.
2. **Reproduce & Debug:** The C service is supposed to compile with `gcc -o /app/server /app/server.c -lpthread`. However, there is a signed integer overflow bug in the calculation function that causes a negative array index and an intermittent segmentation fault when processing the specific `DEVICE_SN` and `MAGIC_KEY` from the new device. Add assertions (`assert()`) to validate intermediate calculations, identify the integer overflow, and fix the C code (likely by changing 32-bit integers to 64-bit integers where appropriate).
3. **Resolve Dependencies:** The system has a conflicting `libjansson` version installed in `/opt/legacy/lib` vs `/usr/lib`. Ensure the server compiles and links correctly against the standard `/usr/lib` version, resolving any compilation or runtime conflicts.
4. **Deploy:** Once fixed, run the compiled service so that it listens on `127.0.0.1:8080`. The service must be running as a background process and successfully handle HTTP GET requests.

The service must accept requests in the format:
`GET /process?sn=<DEVICE_SN>&key=<MAGIC_KEY>`
and return an HTTP 200 OK response with a text payload of the computed positive 64-bit hash. 

Leave the fixed and running server on `127.0.0.1:8080`. Automated verification will send test HTTP requests to this endpoint.