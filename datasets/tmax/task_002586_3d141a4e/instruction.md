You are an operations engineer triaging a critical incident. Our custom data processing service crashed recently in production. We have captured the service logs leading up to the crash.

Your objectives:
1. **Analyze the Logs**: Review `/app/incident.log` to reconstruct the timeline and identify the exact base64-encoded payload that caused the service to crash.
2. **Reverse Engineer Authentication**: The service relies on a pre-compiled object file `/app/data-server/lib/auth.o` for checking API tokens. The original source code for this module is lost. You must reverse engineer this object file to determine the hardcoded secret token required to access the API.
3. **Fix the Vulnerability**: The source code for the main service is located at `/app/data-server/`. The crash is due to a buffer overflow in `/app/data-server/src/processor.cpp` that manifests when processing the malicious payload. Identify the missing bounds check and fix the C++ code to prevent the crash. The buffer should truncate any data exceeding `MAX_PAYLOAD_SIZE` (which is defined as 256 bytes) rather than crashing.
4. **Deploy the Service**: 
   - Compile the service by running `make` inside `/app/data-server/`.
   - Start the service. It must listen for HTTP traffic on `127.0.0.1:8080`.
   - The service must correctly handle HTTP POST requests to the `/process` endpoint. 
   - It must require the `Authorization: Bearer <TOKEN>` header, using the token you discovered in step 2.

Ensure the service remains running in the background so it can be tested. Do not change the existing functional logic of the processor, only add the necessary bounds checking to prevent the buffer overflow.