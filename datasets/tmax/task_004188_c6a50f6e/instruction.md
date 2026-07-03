You are an open-source maintainer reviewing a broken Pull Request. The PR attempts to introduce a new Python package (`filter_grpc`) that runs a gRPC service. This service is supposed to process data by leveraging a high-performance C extension (`filter_core`). Furthermore, the C extension is meant to exactly replicate the behavior of a legacy, proprietary binary executable.

However, the contributor left the PR in a broken state:
1. The `setup.py` build script is broken and fails to compile the C extension. It is missing proper compiler flags for cross-compatibility and linking.
2. The C extension (`filter_core.c`) has logical errors and doesn't implement the correct data transformation.
3. The original proprietary binary is provided at `/app/legacy_filter` (it is a stripped binary). You need to analyze this binary (e.g., using `objdump`, `strings`, or by passing it test inputs) to deduce the data transformation algorithm it applies, and then implement that exact same algorithm entirely in `filter_core.c`. 
4. The gRPC protobuf definition (`service.proto`) and the Python server code (`server.py`) might need minor adjustments to successfully import the fixed C extension and serve requests.

Your task:
- Fix `setup.py` in `/home/user/broken_pr/` so that `pip install .` successfully compiles and installs the `filter_core` C extension.
- Reverse-engineer the algorithmic logic of the stripped binary `/app/legacy_filter`.
- Fix `/home/user/broken_pr/filter_core.c` so it implements this exact transformation algorithm in C. (Do not just `popen` or call the binary from C; you must replicate the logic natively).
- Ensure the gRPC server defined in `/home/user/broken_pr/server.py` can be launched and correctly processes the `ProcessData` RPC as defined in `service.proto`.
- Launch the gRPC server to listen on `127.0.0.1:50051`. Leave it running in the background.

The automated test will verify your solution by acting as a gRPC client, connecting to `127.0.0.1:50051`, and issuing `ProcessData` requests to verify the outputs match the expected transformation natively.