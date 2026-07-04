You are acting as a QA engineer tasked with setting up an isolated test environment for our new embedded metrics collection API. 

We have a vendored copy of a lightweight JSON processing library located at `/app/vendored/cJSON`. Unfortunately, an earlier attempt to patch the Makefile in this vendored package broke the compilation (the `CFLAGS` are overriding the shared library generation). 

Your task involves three main steps:
1. Fix the build system in the vendored `cJSON` package located at `/app/vendored/cJSON` so that it correctly compiles to a shared object (`libcJSON.so`) and installs it into `/app/local/lib` with headers in `/app/local/include`.
2. Write a C-based HTTP server using standard POSIX sockets (or a lightweight library of your choice if you fetch it, though pure C sockets are preferred for this test) that listens on `127.0.0.1:8080`. This server must load the fixed `libcJSON.so`.
3. The server must implement a REST API with the following endpoints:
   - `POST /metrics`: Accepts a JSON array of custom objects containing `{"id": <int>, "value": <string>}`. The server must validate the JSON, sort the objects by `id` in ascending order, base64-encode the `value` strings, and store them in memory using a custom linked-list data structure. Rate limit this endpoint to accept no more than 5 requests per second from the same IP (return HTTP 429 if exceeded).
   - `GET /metrics`: Returns the sorted, base64-encoded metrics in a JSON array.

Ensure the server runs continuously in the background and logs all incoming requests to `/home/user/api.log` in the format: `[TIMESTAMP] METHOD PATH STATUS`.