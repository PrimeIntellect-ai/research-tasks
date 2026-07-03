You are a compliance analyst tasked with generating an audit trail for a legacy authentication system. As part of this effort, we need to integrate an automated vulnerability scanner into the CI/CD pipeline, but the scanner requires valid authentication payloads to test the endpoints. 

The original source code for the payload encoder was lost. However, we have recovered a scanned design document that describes the encoding flow. This document is located at `/app/legacy_auth_spec.png`.

Your task:
1. Analyze the design document (`/app/legacy_auth_spec.png`) using OCR or vision tools (e.g., `tesseract` is pre-installed) to extract the exact authentication payload encoding algorithm.
2. Implement this algorithm in a Python script located at `/home/user/encoder.py`. 
3. Your script must read a raw, unencoded string from standard input (`stdin`), apply the exact multi-stage encoding process described in the image, and print the final encoded token to standard output (`stdout`) without any additional formatting or newlines.
4. The script must handle arbitrary printable ASCII input and correctly perform the payload encoding sequence so we can use it to test authentication flows.

Your implementation must be perfectly bit-exact with the original legacy system. An automated fuzzing system will verify your script against a preserved, stripped binary of the legacy encoder to ensure it is functionally identical for compliance purposes.