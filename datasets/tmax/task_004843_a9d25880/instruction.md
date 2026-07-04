You are a mobile build engineer tasked with creating a local mock backend service for your mobile app's CI/CD pipeline tests. The mobile app needs to test its data payload encoding against a mock server that simulates native ABI libraries (Android/iOS).

Your task is to implement and start this mock HTTP service.

Here are the requirements:
1. **Extract the CI Seed**: We lost the original configuration file, but we have a screenshot of the CI pipeline architecture diagram located at `/app/ci_architecture.png`. You must extract the secret seed from this image (look for a string formatted like `CI_SECRET_SEED: <value>`). You can use OCR tools like `tesseract` which are available on the system.

2. **Compile the Shared Library**: There is a C source file at `/app/encoder.c`. You must compile this into a Linux shared library named `/app/libencoder.so`. This library contains a function `char* encode_payload(const char* payload, const char* platform, const char* seed)`. 

3. **Create the Python Mock Server**: 
   Write and start a Python web server (you may use `Flask`, `FastAPI`, or `http.server`) listening exactly on `127.0.0.1:8080`.

4. **Implement Routing and ABI integration**:
   The server must expose a GET endpoint at exactly:
   `/api/v1/mock/encode`

   It must accept two query parameters:
   - `payload` (string)
   - `platform` (string)

   The endpoint must require an HTTP header for authentication:
   `Authorization: Bearer mobile-ci-token-2024`
   (If the token is missing or incorrect, return a 401 status code).

   When a valid request is received, the Python server must use `ctypes` to load `/app/libencoder.so`, call `encode_payload` passing the URL parameters and the secret seed you extracted from the image.
   
   The endpoint must return a JSON response with status 200:
   `{"status": "success", "result": "<string_returned_by_c_library>"}`

5. Keep the server running in the background or foreground so that the automated pipeline tests can verify the endpoints. Note: ensure your Python code handles character encoding correctly between Python strings and C `char*` pointers.