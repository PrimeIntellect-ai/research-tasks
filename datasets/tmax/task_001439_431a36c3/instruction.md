You are an engineer tasked with porting a legacy data processor to a new minimal microservice environment. 

You have been provided with two main components:
1. A stripped binary tool located at `/app/legacy_processor`. We no longer have the source code, but it processes hex-encoded data payloads and outputs a transformed token.
2. A Bash-based build system located in `/app/builder/`. This build system is responsible for creating a minimal deployment environment in `/home/user/service_root/`, including compiling necessary tools (like `socat` and `jq`) for handling networking and JSON serialization.

Your task consists of three phases:

**Phase 1: Fix the Build System**
The previous engineer left a bug in the build system. When you run `/app/builder/build.sh`, it fails due to a circular import (infinite `source` loop) between the internal scripts. 
Identify and resolve the circular dependency in `/app/builder/` without removing any actual build functionality. Once fixed, run `/app/builder/build.sh` to generate the `/home/user/service_root/` directory.

**Phase 2: Reverse Engineer the Binary**
You must understand how `/app/legacy_processor` behaves. It takes a single command-line argument (a hex string), processes it, and outputs a string. You will need to know how to interface with it for the next step.

**Phase 3: Write the Service**
Inside the generated environment, create a Bash script at `/home/user/service_root/server.sh`. This script must act as an HTTP server listening on `127.0.0.1:9000`. You may use the `socat` and `jq` binaries that the build script placed in `/home/user/service_root/bin/`.

The server must adhere to the following specification:
- Accept `POST` requests to the endpoint `/api/process`.
- The request body will be a JSON object: `{"payload": "<hex_string>"}`.
- Extract the hex string, and pass it as a command-line argument to `/app/legacy_processor`.
- Capture the standard output of the binary.
- Respond with a valid HTTP 1.1 `200 OK` response containing the JSON body: `{"result": "<binary_output>"}`.
- Ensure proper `Content-Length` and `Content-Type: application/json` headers are returned.
- If the binary exits with a non-zero status (e.g., due to invalid hex input), return a `400 Bad Request` with `{"error": "invalid payload"}`.

Once you have written the server, start it in the background so that it is listening on `127.0.0.1:9000`.