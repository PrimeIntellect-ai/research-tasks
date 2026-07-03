You are a performance engineer tasked with debugging and securing a multi-service data processing pipeline. The pipeline currently suffers from severe performance degradation, convergence failures (infinite loops), and occasional JIT compiler crashes caused by malformed or malicious incoming data.

System Architecture (located in `/app/`):
1. **Receiver Service** (`/app/receiver.sh`): Listens on TCP port 8000. It accepts raw telemetry strings and forwards them to the processor.
2. **JIT Processor Service** (`/app/processor.sh`): Listens on TCP port 8001. It dynamically generates a small C program based on the payload, compiles it (invoking `gcc`), and runs a numerical convergence algorithm.
3. **Control Script** (`/app/start_services.sh`): Starts both services and wires them together.

Recently, our pipeline has been failing. Some payloads cause the generated C code to fail compilation with bizarre compiler/linker errors. Other payloads compile fine but cause the numerical algorithm to fail to converge, hanging the processor service entirely and spiking CPU usage. 

Your objective is to build a robust data filter. 
1. Use the provided tools and your delta debugging skills to isolate which payloads cause compiler errors and which cause convergence failures by interacting with `/app/processor.sh` directly.
2. Create a minimal reproducible example for each failure mode to understand the root cause.
3. Write a standalone bash script at `/home/user/filter.sh`.
   - The script must read a single payload from Standard Input (`stdin`).
   - It must exit with code `0` if the payload is safe ("clean").
   - It must exit with code `1` if the payload causes either a compiler error or a convergence failure ("evil").

We have provided a mixed sample of recent traffic in `/app/sample_traffic/`. You can use this to profile the application, observe the errors, and deduce the patterns of "clean" vs "evil" payloads.

Requirements for `/home/user/filter.sh`:
- Must be a bash script (executable, starting with `#!/bin/bash`).
- Must read from `stdin`.
- Must not take longer than 1 second per payload.
- Output absolutely nothing to `stdout` or `stderr` (just the exit code).

An automated test suite will run your `/home/user/filter.sh` against two hidden corpora (one strictly clean, one strictly evil) to verify its accuracy.