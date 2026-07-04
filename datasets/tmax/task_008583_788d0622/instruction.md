You are an engineer tasked with porting a legacy workload constraint validation tool into a minimal container environment. The new architecture uses Protocol Buffers to serialize workload specifications. 

Your objective is to implement the constraint validator in C, define the Protobuf schema, and provide a build script to automate the compilation.

Please complete the following steps:

1. **Protobuf Schema Definition**
   Create a file at `/home/user/workspace/workload.proto`. Define a `Workload` message with the following exact fields:
   - `id` (string)
   - `cpu_cores` (int32)
   - `memory_mb` (int32)
   - `dependencies` (repeated string)

2. **C Implementation**
   Write a C program at `/home/user/workspace/validator.c`. The program must:
   - Accept a single command-line argument: the path to a binary file containing a serialized `Workload` protobuf message.
   - Read and deserialize the message using the `protobuf-c` library.
   - Perform the following constraint satisfaction checks. A workload is only valid if ALL these constraints are met:
     - `cpu_cores` must be greater than 0 and less than or equal to 8.
     - `memory_mb` must be greater than 0 and less than or equal to 2048.
     - The `dependencies` list MUST contain at least `"mysql"` AND `"redis"`. (It is allowed to contain other dependencies as well, but these two must be present).
   - Write the validation result to `/home/user/workspace/validation.log`. The file should contain exactly one line in the following format:
     `Workload <id> verification: <PASS|FAIL>`
     (Replace `<id>` with the parsed workload ID, and use `PASS` or `FAIL` based on the constraints).

3. **Build Script (CI/CD primitive)**
   Create an executable bash script at `/home/user/workspace/build.sh` that automates the build process:
   - It should invoke `protoc-c` to generate the C headers and source files from `workload.proto` into the same directory.
   - It should compile `validator.c` and the generated proto C code into an executable named `validator` in the same directory.
   - Ensure you link against the `protobuf-c` library (using `-lprotobuf-c`).

Note: Assume `protobuf-c-compiler`, `libprotobuf-c-dev`, and `gcc` are already installed on the system. All work must be done inside `/home/user/workspace/`.