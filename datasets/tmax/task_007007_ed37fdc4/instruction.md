You are tasked with setting up a testing pipeline for a polyglot build system. We have a C library that calculates the sorted order of an array of strings, and a Python test suite that needs to supply data to it via FFI (Foreign Function Interface), using data deserialized from Protocol Buffers.

The working directory is `/home/user/polyglot_test`.

Here are the components that already exist in the directory:
1. `data.proto`: A Protocol Buffers definition file containing a `RecordList` message, which holds a repeated list of strings called `payloads`.
2. `sorter.c`: A C source file containing a function `void get_sorted_indices(const char** strings, int count, int* out_indices)`.
3. `input.bin`: A serialized binary Protocol Buffer message of type `RecordList`. The `payloads` in this message are Base64-encoded UTF-8 strings.

Your objective is to write the necessary scripts and commands to process this data, pass it to the C library, and format the output:

1. **Build the C Shared Library:** Compile `sorter.c` into a shared library named `libsorter.so`.
2. **Compile the Protobuf:** Generate the Python protobuf bindings for `data.proto` in the same directory.
3. **Write the Test Script (`test_pipeline.py`):** 
   - Parse `input.bin` using the generated Python protobuf classes.
   - Extract the `payloads`, which are Base64-encoded strings.
   - Decode the Base64 strings to standard UTF-8 Python strings.
   - Use Python's `ctypes` module to pass these decoded strings to the `get_sorted_indices` function in `libsorter.so`. You will need to allocate an integer array of the correct size to receive the `out_indices`.
   - Using the returned `out_indices`, sort the **original decoded UTF-8 strings**.
   - Write the sorted, decoded strings to `/home/user/polyglot_test/sorted_payloads.txt`, with one string per line.
   - Create a new `RecordList` protobuf message containing the newly sorted strings (these MUST be Base64 re-encoded before putting them in the new protobuf message!).
   - Serialize and save this new protobuf message to `/home/user/polyglot_test/output.bin`.

Ensure that you execute your pipeline so that `libsorter.so`, `sorted_payloads.txt`, and `output.bin` are generated successfully.

Note: You can install `protobuf` and `grpcio-tools` via `pip` if they are not already installed to compile the `.proto` file.