You are an AI assistant helping a build engineer manage release artifacts. 

We have received an image containing metadata for our latest build artifact. The image is located at `/app/artifact_info.png`. 

Your task is to:
1. Extract the text from the image `/app/artifact_info.png` using Tesseract OCR. The text will contain a `BUILD_VERSION` and a 2x2 `COEFFICIENTS` matrix (two rows of two integers separated by spaces).
2. Parse the extracted version and use semantic versioning to compare it against a baseline version of `"2.0.0"`.
3. Parse the 2x2 matrix and calculate its determinant.
4. Create and start a Python-based HTTP server listening on `127.0.0.1:8080`.
5. The server must expose a `GET` endpoint at `/api/artifact`.
6. When called, the endpoint must return a JSON response with the following format:
   ```json
   {
     "version": "<extracted_version>",
     "determinant": <calculated_determinant>
   }
   ```
   **Important Rules:**
   - If the extracted `BUILD_VERSION` is strictly greater than `"2.0.0"` (according to semantic versioning), return the actual calculated determinant.
   - If the extracted `BUILD_VERSION` is less than or equal to `"2.0.0"`, the `determinant` field in the JSON response MUST be `0`.

Ensure the server is running in the background and is ready to accept HTTP requests on port 8080 before you finish.