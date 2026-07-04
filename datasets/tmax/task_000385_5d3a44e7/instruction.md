As an automation specialist, you are migrating legacy system configurations into a dynamic, API-driven workflow. We have scanned a physical legacy routing manifest into an image, but we need an automated service that can read its properties and generate standardized configuration templates dynamically.

Your task is to build and run a Go-based HTTP web service that extracts data from this scanned image, normalizes incoming requests, and generates text templates.

Here are the requirements for the workflow:

1. **Extract Manifest Data:** 
   There is a scanned legacy manifest located at `/app/legacy_route_manifest.png`. Use standard OCR tools (like `tesseract`, which is preinstalled) to extract the text from this image.
   The image contains key-value pairs. You need to extract two specific values:
   - The `AuthToken`
   - The `Target`

2. **Build the API Service (Go):**
   Write a Go program that starts an HTTP server listening strictly on `127.0.0.1:9090`.
   The server must expose a single endpoint: `POST /build-config`.

3. **Authentication:**
   The `/build-config` endpoint must require an `Authorization` header in the format: `Bearer <AuthToken>`. Replace `<AuthToken>` with the exact token value extracted from the image. If the token is missing or incorrect, the server should return a `401 Unauthorized` HTTP status.

4. **Normalization & Standardization:**
   The `POST /build-config` endpoint will receive a JSON payload with a single field: `service_name` (a string). 
   Before generating the template, your Go code must normalize the `service_name` by:
   - Converting all characters to lowercase.
   - Removing any non-alphanumeric characters (strip anything that is not `a-z` or `0-9`).

5. **Template-Based Text Generation:**
   Using Go's built-in `text/template` package, generate a YAML configuration block in the exact format below, substituting the normalized service name and the `Target` you extracted from the image:

   ```yaml
   service: <normalized_service_name>
   target: <Target_extracted_from_image>
   managed_by: automation_specialist
   ```
   
   The HTTP response body must be exactly this generated YAML string, with a `200 OK` status code.

6. **Execution:**
   Write your Go code to `/home/user/server.go`.
   Compile and start your server in the background so that our automated test suite can verify it via HTTP requests. Ensure the server stays running.