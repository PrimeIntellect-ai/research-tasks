You are a mobile build engineer maintaining our CI/CD pipelines. We have a legacy, proprietary native build tool used for asset compilation, located at `/app/bin/asset_compiler`. This tool is a stripped binary and is notoriously fragile. Recently, it has been crashing during the pipeline when processing certain generated native object files, causing pipeline failures. 

We need to implement a pre-flight validation step in our build pipeline to intercept and reject these "evil" files before they reach the `asset_compiler`.

Your task is to:
1. **Analyze the Failure:** We have collected a set of generated `.bin` asset files. Some cause the compiler to crash, others don't.
   - Go to `/home/user/workspace/` where you will find a `Makefile` and several assembly (`.s`) and C source files.
   - Run `make` to compile the corpora. This will generate `.bin` files in `/home/user/workspace/corpus/clean/` and `/home/user/workspace/corpus/evil/`.
   - Test these files against `/app/bin/asset_compiler` (usage: `/app/bin/asset_compiler <file>`). Figure out the precise byte-level pattern or instruction sequence present in the `evil` corpus that triggers the crash (e.g., specific hardware instructions or invalid opcodes).

2. **Create a gRPC Validator Service:** 
   - A Protobuf definition is provided at `/home/user/workspace/pipeline.proto`.
   - Compile this protobuf for Python.
   - Implement a Python gRPC server (in `/home/user/workspace/validator_server.py`) that implements the `AssetValidator` service.
   - The `ValidateAsset` RPC must take the bytes of an asset, scan it for the crash-inducing pattern you identified, and return `is_valid = False` if it contains the pattern, or `is_valid = True` if it is safe.

3. **Deploy the Service:**
   - Start your Python gRPC server so it listens in the background on `localhost:50051`.
   - Write a short Python test client `test_client.py` to verify that your server correctly processes the corpora.
   - Leave the `validator_server.py` process running on port 50051 when you are finished.

**Requirements:**
- Do not modify `/app/bin/asset_compiler`.
- Your Python gRPC server must run on `0.0.0.0:50051` or `localhost:50051`.
- It must perfectly distinguish the clean corpus from the evil corpus based on the malicious byte sequence.
- All Python dependencies (e.g., `grpcio`, `grpcio-tools`, `capstone`) can be installed via `pip`.