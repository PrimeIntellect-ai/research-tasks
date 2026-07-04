We are in the process of porting our legacy telemetry validation tool to run inside a minimal Linux container. Our system receives binary telemetry traces serialized via Protocol Buffers. Recently, the CI pipeline has been failing because the original Python validator is too heavy and has dependency ordering issues in the minimal image. We are rewriting the validator in C, but the engineer assigned to it left it incomplete and the build system is broken.

Your objective is to fix the build system, implement the missing validation logic using a C state machine, and ensure it correctly categorizes traces.

Here is what you have in `/app/`:
1. `/app/schema/trace.proto`: The protocol buffer definition for the telemetry traces.
2. `/app/src/validator.c`: The skeleton of the C program. It should take a single command-line argument (the path to a binary protobuf file), deserialize it, and validate it.
3. `/app/Makefile`: A broken Makefile. It currently fails to compile the C bindings for the protobuf and has linking errors.
4. `/app/docs/statemachine.png`: An image snippet we recovered from an old wiki. It contains the exact state machine rules that define a "valid" sequence of event types in a trace. You will need to extract the rules from this image (e.g., using `tesseract`).
5. `/app/corpus/clean/`: A directory containing binary protobuf files that represent valid traces. Your program MUST accept all of these.
6. `/app/corpus/evil/`: A directory containing binary protobuf files that violate the state machine rules or are otherwise malformed. Your program MUST reject all of these.

Requirements:
- Fix `/app/Makefile` so that running `make -C /app` successfully builds the executable `/app/build/validator`. You must use `protobuf-c`.
- Complete `/app/src/validator.c`. It must deserialize the `Trace` message using the generated C bindings.
- Implement the state machine parser in `/app/src/validator.c` based exactly on the rules found in `/app/docs/statemachine.png`.
- The compiled executable `/app/build/validator <file_path>` must exit with status `0` if the trace is completely valid, and status `1` if it is invalid, malformed, or cannot be read.

Ensure your compiled program correctly acts as a strict classifier. Our automated verification suite will test `/app/build/validator` against the hidden corpora. You must achieve a 100% pass rate (all clean accepted, all evil rejected).