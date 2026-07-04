I am currently dealing with a legacy Python 2 data processing service, and I need your help writing a Bash script to automate its migration to Python 3 and Protobuf 3.

The legacy application is located at `/home/user/legacy_app` and consists of two main files:
1. `/home/user/legacy_app/schema.proto`: A `proto2` schema defining a data processing gRPC service.
2. `/home/user/legacy_app/service.py`: A Python 2 script that runs a dual-protocol server: it hosts a gRPC server to process data and a `BaseHTTPServer` that parses URL parameters to trigger internal processing (URL routing).

Your task is to write a Bash script at `/home/user/upgrade_pipeline.sh` that performs the following steps automatically:
1. Copies the `/home/user/legacy_app` directory to `/home/user/modern_app`.
2. Uses standard Bash text processing tools (like `sed` or `awk`) to upgrade `/home/user/modern_app/schema.proto` to `proto3`. You must change the syntax declaration to `"proto3"` and remove any `required` field labels (as they are not supported in proto3).
3. Installs the necessary Python 3 gRPC tools (`grpcio` and `grpcio-tools` via `pip`).
4. Compiles the upgraded `schema.proto` into Python 3 gRPC bindings inside the `/home/user/modern_app` directory.
5. Upgrades `/home/user/modern_app/service.py` to Python 3 syntax using `sed` or `awk`. Specifically:
   - Change `import BaseHTTPServer` to `import http.server as BaseHTTPServer`.
   - Change `import urlparse` to `import urllib.parse as urlparse`.
   - Convert Python 2 `print "..."` statements to Python 3 `print("...")` function calls.
   - Update any string/bytes handling if the gRPC server expects strings instead of bytes.
6. Starts the upgraded Python 3 service in the background. The service will bind to port 8080 (HTTP) and 50051 (gRPC).
7. Uses `curl` to send a GET request to `http://127.0.0.1:8080/process?payload=migrate_me` and saves the exact HTTP response body to `/home/user/migration_result.log`.
8. Kills the background Python 3 service before the script exits.

Ensure your Bash script has executable permissions (`chmod +x`). Do not manually modify the files; your Bash script must perform all the migrations and validations.