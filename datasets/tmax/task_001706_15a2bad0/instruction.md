You are tasked with investigating and mitigating a severe memory leak in a long-running C++ telemetry aggregation service. The service intermittently crashes due to OOM (Out Of Memory) errors after running for several hours. 

You have been provided with log excerpts from three interacting microservices (`gateway`, `telemetry-aggregator`, and `storage`) located in `/home/user/logs/`. You must reconstruct the log timeline across these services to identify the exact sequence of events and payload characteristics that trigger the intermittent failure.

The `telemetry-aggregator` relies heavily on a third-party JSON parsing package for payload deserialization. The source for this package is vendored in your environment at `/app/vendor/json11/` (a widely used C++11 JSON library).

### Your Objectives

**1. Root Cause Analysis & Convergence Failure Repair**
The memory leak is caused by a convergence failure in the vendored `json11` library when processing a very specific type of malformed payload. When encountering this payload, the parser enters an error-handling path that allocates memory but fails to converge on a clean exit, leaking the allocated error context.
- Identify the bug in `/app/vendor/json11/json11.cpp`.
- Apply a code fix to the library so that parsing the malformed payload correctly returns an error without leaking memory.

**2. Adversarial Payload Detector**
To protect downstream legacy instances of the service that cannot be updated immediately, you must write a standalone C++ payload filter. 
- Create your source file at `/home/user/json_filter.cpp`.
- Compile it to an executable located at `/home/user/json_filter`.
- Your executable must accept a single command-line argument: the absolute path to a JSON file (e.g., `/home/user/json_filter /path/to/payload.json`).
- The program must analyze the file's contents and determine if it represents the "evil" payload type that triggers the memory leak.
- **Exit Code Requirements:**
  - Exit `0` (Success) if the payload is safe/clean.
  - Exit `1` (Error) if the payload contains the leak-triggering malformed structure.

You will need to create a minimal reproducible example locally to test your fix and your filter. Use standard C++ tools (g++, valgrind) available in the environment to verify your memory leak fix.

Ensure your compiled executable `/home/user/json_filter` is statically or dynamically linked correctly so it can be executed standalone by our automated verification suite.