You are an engineer tasked with repairing and configuring a polyglot data transformation pipeline. The system consists of a Go-based API gateway that concurrently dispatches jobs, and a C-based backend worker that performs the actual data transformation. 

Currently, the system is broken: the C build system (Makefile) is corrupted, the C parsing logic has bugs, and the services are not properly configured to communicate with each other.

Your objectives are:

1. **Repair the C Build System and Code:**
   Navigate to `/app/c_worker/`. You will find a broken `Makefile` and two source files: `transform.c` (contains the transformation logic) and `main_cli.c` (a CLI wrapper). 
   - Fix the `Makefile` so that running `make` produces an executable named `transformer`.
   - The C program is supposed to read a custom structured format from `stdin`: a 4-byte little-endian integer representing the payload length, followed by the actual ASCII data. It must apply a standard ROT-13 transformation to all alphabetical characters and write the raw resulting bytes to `stdout`.
   - There are parsing and memory management bugs in `transform.c` causing segfaults and incorrect output. Debug and fix the code. You have access to a reference binary at `/app/reference/transformer_oracle` which behaves exactly as the repaired program should.

2. **Configure the Multi-Service Architecture:**
   The Go gateway is located in `/app/gateway/`. It is pre-compiled as `gateway_service`. It spawns goroutines to handle incoming HTTP requests and forwards the data over a raw TCP socket to the C worker daemon.
   - The C worker daemon code is in `/app/c_worker/daemon.c`. Fix the `Makefile` to also build an executable named `worker_daemon` from this file, which links against `transform.c`. The daemon natively listens on TCP port `9000`.
   - You need to configure the Go gateway to communicate with this daemon. Edit `/app/gateway/.env` and set the correct values so the gateway binds to port `8080` and sends worker requests to `127.0.0.1:9000`.

To complete the task, ensure that:
- `/app/c_worker/transformer` is compiled and its standard I/O behavior perfectly matches `/app/reference/transformer_oracle`.
- `/app/c_worker/worker_daemon` is compiled.
- `/app/gateway/.env` is correctly configured.

You do not need to start the services in the background; our automated test suite will boot them up using your compiled binaries and configuration files to verify the end-to-end workflow.