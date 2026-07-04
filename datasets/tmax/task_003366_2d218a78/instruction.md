I am porting an old Python-based configuration validator to a minimal container environment. To reduce memory overhead and fix some CI issues we've been having with Python import ordering, we are rewriting the service in Go.

Our legacy system uses physical printed configuration cards that are scanned into the system. You are provided with a scanned configuration card at `/app/config.png`.

Your task is to write a Go network service (`/app/server.go`) that does the following:

1. **Configuration Extraction**:
   Extract the text from `/app/config.png` using `tesseract` (which is preinstalled in the environment). 
   The OCR output will contain:
   - A rate limit rule in the format `RATE_LIMIT=<number>`
   - A list of valid access keys under a line saying `VALID_KEYS:`

2. **HTTP Service**:
   Start an HTTP server listening on exactly `127.0.0.1:8080`.
   Implement a single endpoint: `POST /validate`

3. **Request Validation**:
   The endpoint will receive a JSON payload containing an array of keys, for example: `{"keys": ["alpha", "beta"]}`.
   You must validate that *all* keys provided in the request array exist in the `VALID_KEYS` list extracted from the image. (Perform necessary sorting/diffing internally to efficiently verify this).
   - If all keys are valid, return HTTP `200 OK`.
   - If any key is missing or invalid, return HTTP `400 Bad Request`.

4. **Rate Limiting**:
   Implement a strict global rate limit based on the `RATE_LIMIT` value extracted from the image.
   The server should allow exactly `RATE_LIMIT` requests to the `/validate` endpoint. 
   Any subsequent requests (whether they have valid keys or not) must be rejected with HTTP `429 Too Many Requests`.

Write the Go code, compile it, and start the server in the background so it is actively listening on port 8080 when you finish. Ensure your server correctly leverages Go's standard `net/http` and `encoding/json` libraries. Do not use external Go web frameworks.