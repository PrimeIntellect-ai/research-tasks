You are a developer tasked with organizing project files. To identify duplicates and prepare for a new indexing microservice, you need to write a custom file signature algorithm in Bash, define its gRPC interface, and write a property-based test for it.

Complete the following three steps:

1. **Numerical Algorithm Implementation (Bash)**
Create a script at `/home/user/compute_sig.sh` that takes a single file path as its argument.
The script must read the file and compute a custom numerical signature: the sum of the unsigned byte values (0-255) of all bytes in the file, modulo 256.
The script must print ONLY this final integer (0-255) to standard output. 
Make sure the script is executable.

2. **gRPC and Protobuf Service Design**
Create a Protocol Buffers file at `/home/user/file_service.proto`.
Use `syntax = "proto3";`.
Define a package named `fileorg`.
Define a service named `FileOrganizer` with an RPC method `ComputeSignature`.
The method should take a message named `FileRequest` and return a message named `SignatureResponse`.
The `FileRequest` message must have a single string field `filepath` (tag 1).
The `SignatureResponse` message must have a single uint32 field `signature` (tag 1).

3. **Property-Based Testing (Bash)**
Create a script at `/home/user/prop_test.sh`.
This script should test the mathematical property of determinism: a file and its exact copy must yield the exact same signature.
The script must perform 5 iterations. In each iteration:
- Generate a random file with a random length (between 10 and 100 bytes) containing random bytes (e.g., from `/dev/urandom`).
- Create an exact copy of this file.
- Run `/home/user/compute_sig.sh` on both files.
- If the signatures differ at any point, print "FAIL" and exit with code 1.
If all 5 iterations pass, print "PASS" to standard output and exit with code 0.
Make sure the script is executable.