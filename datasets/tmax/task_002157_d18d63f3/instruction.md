You are acting as a build engineer managing an artifact patching system. 

We have a vendored package located at `/app/vendored/patch_manager` (a simple Python tool for applying unified diffs to text artifacts). Unfortunately, the package is broken due to a deliberate perturbation in its source code (a syntax or logic error). 

Your task is to build a gRPC-based artifact patching service with a reverse proxy in front of it.

Step 1: Fix the Vendored Package
Inspect the Python code in `/app/vendored/patch_manager`. Identify and fix the bug so that it correctly applies unified diffs. You can test it by running its internal `make test` or running the module directly.

Step 2: gRPC Protocol Design
Create a Protobuf definition file at `/app/artifact.proto`.
It must define a package `artifact` with a service `PatchService`.
The service must expose a single RPC method: `ApplyPatch`.
The request message `PatchRequest` must contain two string fields: `original_content` (tag 1) and `patch_content` (tag 2).
The response message `PatchResponse` must contain a single string field: `patched_content` (tag 1).

Step 3: Python gRPC Server
Compile the protobuf file to Python using `grpcio-tools`.
Write a Python gRPC server in `/app/server.py` that implements `PatchService`. 
It must import and use the fixed `/app/vendored/patch_manager` to apply the `patch_content` to the `original_content`. If the patch fails, return an empty string.
The gRPC server must listen in insecure mode on `127.0.0.1:50051`.
Start the server in the background.

Step 4: Reverse Proxy Configuration
We need to expose this gRPC service through an Nginx reverse proxy using gRPC proxying.
Create an Nginx configuration file at `/app/nginx.conf`.
The Nginx server must listen on `127.0.0.1:8080` (HTTP/2) and proxy all requests to `grpc://127.0.0.1:50051`.
Run Nginx in the background using this configuration.

When you are finished, ensure both the Python gRPC server and the Nginx proxy are running. Keep them running so that our automated test suite can send gRPC requests to `127.0.0.1:8080` and verify the artifact patching.