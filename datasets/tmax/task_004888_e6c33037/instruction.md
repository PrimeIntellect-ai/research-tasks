You are an integration developer working on a backend service that evaluates proprietary encoded expressions. We have a legacy stripped binary, `/app/bin/legacy_evaluator`, which correctly implements this evaluation. 

We are migrating this functionality to a Python API via a native C-extension, located at `/home/user/api_integration/legacy_decoder/`. Unfortunately, the migration has stalled:
1. The `setup.py` build configuration is broken and fails to compile the C extension.
2. The C extension (`src/decoder.c`) suffers from memory safety issues (Undefined Behavior like out-of-bounds reads) and segfaults on certain inputs.
3. The C extension's character decoding and expression parsing logic does not match the legacy binary. The binary takes a custom-encoded string (which you must reverse-engineer or black-box analyze), decodes it into a Reverse Polish Notation (RPN) mathematical expression, and evaluates it.

Your task is to:
1. Fix the build system in `/home/user/api_integration/legacy_decoder/setup.py` so the package can be installed via `pip install -e .`.
2. Debug and patch `src/decoder.c` so that it safely parses the input without crashing and perfectly mirrors the decoding and RPN evaluation logic of the legacy binary.
3. Write a CLI wrapper script at `/home/user/api_integration/run_api.py` that takes a single encoded string as a command-line argument, processes it using the `legacy_decoder` Python module, and prints the integer result to standard output (or exactly mimics the error output of the oracle if the expression is invalid).

Your final `run_api.py` must behave bit-for-bit identically to `/app/bin/legacy_evaluator` for all valid and invalid inputs.