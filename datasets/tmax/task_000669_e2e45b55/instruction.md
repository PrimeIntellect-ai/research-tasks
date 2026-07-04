You are a support engineer tasked with collecting diagnostics and resolving an issue for a customer's OCR microservice.

The customer reported that a specific image they uploaded is causing their Python backend to crash with a database query error, but they didn't provide the logs. They only provided the uploaded image, which is located at `/app/customer_upload.png`.

Your objectives are:
1. **Analyze the Image:** Extract the text from `/app/customer_upload.png` to understand what data is causing the issue. (Tesseract is available on the system).
2. **Diagnose the Bug:** Review the customer's backend script located at `/home/user/server.py` (you will need to create and fix this based on the standard boilerplate). The issue is known to be a poorly constructed SQL query or text parsing issue that fails when encountering the specific string pattern found in the image.
3. **Create an MRE:** Create a minimal reproducible example script at `/home/user/mre.py` that demonstrates the bug using the extracted text, and then proves your fix works by printing "SUCCESS: <extracted_text>" to stdout.
4. **Deploy the Fixed Service:** Fix the issue in the microservice and start it. The service must be a Python HTTP server (e.g., using `Flask` or `http.server`) running on `127.0.0.1:8080`.
    - It must expose a `POST /process` endpoint.
    - It must accept an image file in the request body (raw binary or multipart form data).
    - It must require an `Authorization` header with the exact value: `Bearer diag-token-xyz`.
    - It must run OCR on the uploaded image and return a JSON response in the format: `{"extracted_text": "<text>"}` (with whitespace stripped).

Run the server in the background so it remains active. Do not stop the server once it is running, as it will be tested by an automated verifier.