You are an engineer setting up a miniature polyglot build system and benchmarking pipeline from scratch.

Your objective is to design a Protocol Buffer schema, write a Bash script that acts as the build system to compile the schema, generate serialization/deserialization code, and benchmark the deserialization performance.

Complete the following steps:

1. Create a directory `/home/user/build_system/`.
2. Inside it, design a protobuf file named `schema.proto` (syntax = "proto3") that satisfies these constraints:
   - Define a message named `ConfigRequest` with two fields: a string named `key` (field number 1) and an int32 named `value` (field number 2).
   - Define a message named `ConfigResponse` with one field: a bool named `success` (field number 1).
   - Define a gRPC service named `Configurator` with a single RPC method named `UpdateConfig` that takes a `ConfigRequest` and returns a `ConfigResponse`.
3. Create an executable Bash build script at `/home/user/build_system/build.sh`. When run, this script must:
   - Use `protoc` to compile `schema.proto` into Python bindings in the same directory (`/home/user/build_system/`).
   - Use a Here-Doc (`cat << 'EOF' > ...`) to dynamically generate a Python script named `serialize.py` in the same directory. This script must import the generated protobuf module, instantiate a `ConfigRequest` with `key` set to "max_workers" and `value` set to `42`, and serialize it to a binary file named `/home/user/build_system/payload.bin`.
   - Execute `serialize.py` using `python3` to produce the `payload.bin` file.
   - Use another Here-Doc to dynamically generate a Python script named `deserialize.py`. This script must read `/home/user/build_system/payload.bin` and deserialize it back into a `ConfigRequest` object 1000 times in a loop.
   - Execute `deserialize.py` using `python3` and benchmark its execution using the `time` command. Write the standard error output of the `time` command to `/home/user/build_system/bench.log` (e.g., `time python3 deserialize.py 2> bench.log` or similar, ensuring the timing output is captured in the log).

Ensure `/home/user/build_system/build.sh` is executable (`chmod +x`). 
You may assume `protoc` and the python `protobuf` package are already installed on the system.