You are an automation specialist creating a data processing pipeline for legacy IoT devices. 

We have a proprietary legacy binary located at `/app/telemetry_decoder`. This binary takes a raw hexadecimal payload via standard input (stdin) and outputs a decoded JSON string representing sensor readings (temperature, pressure, and humidity). We do not have the source code for this binary, but we know it processes the data deterministically.

Your task is to create a Python-based HTTP middleware service that processes incoming telemetry streams, decodes them, aggregates the data, and generates alerts based on deviations from a baseline.

Here are the requirements for your service:
1. **HTTP Server:** Create a Python HTTP server (using `http.server`, `Flask`, `FastAPI`, or any standard library/framework you can install via pip locally) listening exactly on `127.0.0.1:8080`.
2. **Endpoint:** Expose a `POST /process` endpoint. The endpoint will receive JSON payloads in the following format:
   `{"timestamp": "YYYY-MM-DDTHH:MM:SSZ", "payload": "<hex_string>"}`
3. **Decoding:** For each request, pass the `<hex_string>` to the stdin of `/app/telemetry_decoder`. It will print a JSON object to stdout, like `{"temp": 22.5, "pressure": 1010.0, "humidity": 55.0}`. Parse this JSON.
4. **Time-based Bucketing:** Round down the `timestamp` to the nearest 5-minute bucket. For example, `2023-10-01T12:04:15Z` becomes `2023-10-01T12:00:00Z`.
5. **Distance Computation:** Calculate the Euclidean distance between the received sensor readings `[temp, pressure, humidity]` and the expected baseline vector `[20.0, 1013.25, 50.0]`.
6. **Alert Generation:** If the computed Euclidean distance is strictly greater than `10.0`, generate an alert message using this exact template:
   `"ALERT: Deviation of {distance} detected at {bucket}."` (where `{distance}` is rounded to 2 decimal places, and `{bucket}` is the 5-minute bucketed timestamp). If the distance is 10.0 or less, the alert should be `null`.
7. **Response:** Return a JSON response with an HTTP 200 status code:
   `{"bucket": "<bucketed_timestamp>", "distance": <float_rounded_to_2_decimal_places>, "alert": "<alert_string_or_null>"}`

Start the server in the background or leave it running in your final command so that it can be tested. Ensure your script is saved at `/home/user/middleware.py`.