You are a mobile build engineer tasked with fixing and orchestrating our internal build dependency and artifact caching pipeline. 

Our build system relies on three cooperating services:
1. **Dependency Graph Resolver** (Python, running on port 8001): Parses an internal graph of build targets and resolves build order.
2. **Artifact Checksum Engine** (C++, running as a FastCGI service on port 8002): Calculates custom error-correcting checksums (Reed-Solomon based) for build artifacts to ensure memory-safe binary caching.
3. **Cache Coordinator** (Redis, running on port 6379): Stores the resolved graph state and artifact checksums.

Currently, the pipeline is failing in two ways:
First, the Artifact Checksum Engine (source located at `/home/user/build_tools/checksum_engine.cpp`) crashes with segmentation faults on certain large artifact inputs due to undefined behavior and memory leaks. You need to debug and repair the memory safety issues in this C++ code. The engine must compile cleanly with `g++ -O2 -fsanitize=address` without triggering any warnings or ASAN errors during execution.

Second, the system services are not communicating correctly. You need to configure the Multi-Service Build Pipeline. The services are located in `/home/user/services/`. You must adjust the startup scripts (`/home/user/services/start_pipeline.sh`) and environment variables so that the Dependency Resolver can query the Checksum Engine and cache results in Redis. 

Once repaired and orchestrated, the Checksum Engine's core calculation logic must behave exactly like our reference implementation binary provided by the vendor.

Finally, write a CI/CD pipeline script at `/home/user/ci_verify.sh` that:
1. Starts the Redis server, Checksum Engine, and Dependency Resolver.
2. Sends a POST request to `http://localhost:8001/resolve` with the payload `{"target": "mobile_app_v2"}`.
3. Logs the JSON response to `/home/user/build_result.log`.

Ensure that all services start properly and that the checksum logic exactly matches the reference oracle for any arbitrary byte array input.