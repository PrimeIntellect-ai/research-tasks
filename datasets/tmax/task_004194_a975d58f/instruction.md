We are maintaining the mobile build pipeline, and we've been running into frequent build failures caused by conflicting peer dependencies in our React Native modules. To fix this dynamically, our mobile architecture team built a proprietary dependency constraint solver written in C++. 

You have been provided with this compiled solver as a stripped binary located at `/app/peer_resolver`. 

Your task is to write and start a lightweight HTTP wrapper service around this binary so our CI/CD pipeline can query it over the network. You can write this service in any language (Python, Node.js, etc.), but it must be running and listening on `127.0.0.1:9090` before you finish.

The service must expose the following two endpoints:

1. **`POST /resolve`**
   - **Request Payload:** JSON format containing two base64-encoded strings:
     ```json
     {
       "graph_b64": "<base64_encoded_binary_graph>",
       "manifest_b64": "<base64_encoded_package_json>"
     }
     ```
   - **Action:** 
     1. Decode both base64 strings.
     2. Save them to temporary files.
     3. Execute the solver binary: `/app/peer_resolver <path_to_decoded_graph> <path_to_decoded_manifest>`
     4. The binary will output a standard Unified Diff (`.patch` format) to `stdout` which resolves the conflicts.
     5. Apply this diff to the decoded manifest to generate the resolved manifest.
   - **Response Payload:** JSON containing the final patched manifest as a string:
     ```json
     {
       "patched_manifest": "<string_content_of_the_patched_manifest>"
     }
     ```

2. **`GET /benchmark`**
   - **Action:** Our CI runners need to monitor solver performance degradation. When this endpoint is hit, the service must execute `/app/peer_resolver /app/sample_graph.bin /app/sample_manifest.json` exactly 50 times sequentially.
   - **Response Payload:** JSON containing the average execution time in milliseconds:
     ```json
     {
       "avg_time_ms": 12.5
     }
     ```

Make sure the server is left running in the background listening on port 9090 on `127.0.0.1`. Do not add any authentication.