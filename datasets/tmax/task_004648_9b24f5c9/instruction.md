You are a DevSecOps engineer responsible for enforcing policy as code across our microservices. We have an internal Python library, `secscanner`, which performs automated vulnerability scanning and sensitive data redaction on configuration files. 

Recently, we vendored the source of `secscanner` version 1.0.4 into our environment at `/app/secscanner-1.0.4`. However, a developer accidentally introduced a perturbation in the `secscanner/redactor.py` file, causing it to fail when decoding Base64 encoded payloads before redaction. Furthermore, the library's `setup.py` has an incorrect dependency listed.

Your task is to:
1. Fix the `secscanner` package in `/app/secscanner-1.0.4` so that it correctly decodes Base64 payloads and installs successfully.
2. Build a Python service that uses this library to expose two endpoints:
   a. An HTTP server running on `127.0.0.1:8080`. It must accept POST requests at `/scan` with a JSON body `{"filepath": "<path_to_file>", "encoded_payload": "<base64_string>"}`.
   b. A gRPC server running on `127.0.0.1:50051`. It must implement a `Scanner` service with a `ScanPayload` RPC taking the same parameters.
3. The service must first check the file permissions of the given `filepath`. If the file is world-readable (e.g., `0o644` or `0o777`), the service must return a security exception (HTTP 403 or gRPC PERMISSION_DENIED).
4. If the permissions are strict (e.g., `0o600`), the service should use the fixed `secscanner` library to decode the `encoded_payload`, redact any sensitive API keys (matching the regex `AKIA[0-9A-Z]{16}`), and write the redacted payload into the `filepath`.
5. The service must return a success response (HTTP 200 or gRPC OK) with the string `"Redaction complete"` upon successful writing.

A test gRPC proto file is provided at `/home/user/scanner.proto`.
Please write the service implementation in `/home/user/policy_service.py` and leave it running in the background.

Ensure that the service correctly handles both HTTP and gRPC protocols, and enforces the file permission access control strictly.