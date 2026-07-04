You are acting as a release manager preparing a deployment automation service. We have a custom configuration language (a simple DSL) used in our CI/CD pipelines, and we need a webhook service to interpret these configurations and return a merged, sorted JSON deployment manifest. 

Furthermore, our security team provided the deployment authorization token as an image of a scanned physical token.

Your task:
1. Locate the token image at `/app/auth_token.png`. Use OCR (e.g., `tesseract`, which is preinstalled) to extract the text from this image. This text is the authorization token. Strip any trailing whitespace or newlines.
2. Write and run a Python HTTP service listening on `0.0.0.0:8080`.
3. The service must expose a `POST /deploy` endpoint.
4. The endpoint must require an `Authorization: Bearer <token>` header, where `<token>` is the exact string extracted from the image. If the header is missing or incorrect, return a `401 Unauthorized` HTTP status.
5. The request body will contain a plain-text script written in our custom DSL.
6. Your service must implement an interpreter for this DSL. The interpreter starts with a base configuration dictionary:
   `{"version": "1.0", "environment": "production", "debug": false}`
7. The DSL supports the following commands (one per line):
   - `SET <key> <value>` : Sets the string `<value>` for `<key>`.
   - `NUM <key> <value>` : Sets the integer `<value>` for `<key>`.
   - `MERGE <json_string>` : Deserializes the inline `<json_string>` and merges its keys into the current configuration (overwriting existing keys if they conflict).
   - `DELETE <key>` : Deletes `<key>` from the configuration if it exists.
   (Ignore empty lines. Words are separated by a single space for `SET` and `NUM`, while `MERGE` takes the rest of the line as JSON).
8. After executing the DSL script, the service must sort the final configuration dictionary by its keys alphabetically.
9. Serialize the final dictionary to JSON and return it as the HTTP response body with a `200 OK` status and `Content-Type: application/json`.

Leave the service running in the foreground or background so that our CI/CD verifier can send requests to it. You may install any Python packages (like Flask or FastAPI) using pip if you prefer, or use the standard library.