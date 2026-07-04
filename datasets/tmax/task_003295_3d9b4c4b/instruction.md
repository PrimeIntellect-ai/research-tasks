I am setting up a polyglot data processing pipeline. Our core data crunching is done in C, which we intend to expose to other languages via FFI (using a shared library). However, the initial C build setup is broken. 

In `/home/user/polyglot-data`, there is a small C project that serializes and deserializes a custom key-value data format (e.g., `id:1,value:50`). It takes an input string, multiplies the `value` by 2, and returns the serialized result.

The project contains:
- `processor.h` and `processor.c`: The core library logic.
- `main.c`: A CLI wrapper to test the library.
- `Makefile`: The build script.

Currently, running `make` fails due to compilation and linking errors. 

Your task is to:
1. Fix the `/home/user/polyglot-data/Makefile` so that it successfully builds a shared library named `libprocessor.so` (ensure the code is compiled as position-independent) and an executable named `app` that dynamically links against `libprocessor.so`.
2. Write a property-based testing shell script at `/home/user/polyglot-data/test.sh`. The script should:
   - Generate 10 random test cases with the format `id:<random_id>,value:<random_value>` (where both are integers).
   - Run the compiled `app` with each generated string as its first argument.
   - Save the raw standard output of these 10 executions into `/home/user/polyglot-data/output.log` (one execution output per line).
   - Ensure `app` can find the shared library at runtime.

Run your `test.sh` script to produce the final `output.log` file.