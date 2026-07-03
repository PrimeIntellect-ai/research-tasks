You are a data engineer responsible for fixing and deploying a local ETL microservice. 

We have a pre-vendored C++ ETL microservice source package located at `/app/etl-worker`. This service is designed to receive batches of unstructured text logs via HTTP, process them in parallel, extract specific transaction IDs, and return a JSON array of the extracted features.

However, the package is currently broken:
1. **Build Failure:** The project fails to compile/link correctly due to a misconfigured `Makefile`. The service utilizes C++11 standard library threads (`std::thread`, `std::async`) for parallel data processing, but the build configuration is missing the necessary linker flags for threading.
2. **Feature Extraction Bug:** The logs contain transaction strings that often span multiple lines (embedded newlines). The current regex pattern in `src/extractor.cpp` (designed to find transaction IDs matching the format `TXN-<4 uppercase letters>-<5 digits>`, e.g., `TXN-ABCD-12345`) is completely broken and silently drops or fails to match IDs when they are adjacent to newline characters or contain slightly varied whitespace. You must rewrite the `std::regex` pattern to correctly and robustly extract these IDs, ignoring surrounding whitespace and handling the multi-line nature of the raw payload.

Your task is to:
1. Navigate to `/app/etl-worker`.
2. Fix the `Makefile` so the C++ project builds successfully when you run `make`.
3. Fix the regular expression in `src/extractor.cpp` to correctly extract the transaction IDs.
4. Compile the project.
5. Start the service. The service must listen on `127.0.0.1:8080` (the port and host are configurable via command-line arguments: `./etl_server 127.0.0.1 8080`).

Keep the service running in the background. Once the service is running, it will expose an HTTP POST endpoint at `/extract`. Our automated systems will send raw text payloads to this endpoint and verify that the correct transaction IDs are returned in a JSON list.