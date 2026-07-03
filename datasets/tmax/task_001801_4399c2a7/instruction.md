You are helping a developer organize a messy gRPC project directory containing several Protocol Buffer (`.proto`) files. The project specifically focuses on mathematical operations and error-correcting codes.

Your task is to identify specific service definitions, organize the files based on their protobuf package names, and generate a checksum manifest.

Here are the exact requirements:
1. Search through the directory `/home/user/grpc_project/` for all `.proto` files.
2. Identify only the `.proto` files that contain an RPC definition related to mathematical error correction. Specifically, look for files containing either the word `Hamming` or the word `Checksum` (case-sensitive) anywhere in the file.
3. For each matching file, extract its protobuf package name. The package name is defined in the file like `package some.name.space;`.
4. Move these matching files into a new directory structure under `/home/user/organized_protos/`. The directory structure must reflect the package name, replacing dots with slashes. For example, if a file has `package network.ecc;`, it should be moved to `/home/user/organized_protos/network/ecc/`. Keep the original filename.
5. Finally, calculate the SHA-256 checksum of each moved file. Create a manifest file at `/home/user/manifest.txt`. Each line of the manifest must contain the SHA-256 checksum, two spaces, and the new absolute path of the file. The lines in the manifest must be sorted alphabetically by the file path.

Example `manifest.txt` format:
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /home/user/organized_protos/network/ecc/fileA.proto
...

Only use standard shell tools (bash, grep, awk, sha256sum, mkdir, mv, sort, etc.) to complete this task. Do not modify the contents of the `.proto` files.