You are helping to fix a build pipeline for a multi-file Rust project that compiles gRPC services. Currently, the project fails to compile and crashes our backend build servers because users are uploading malicious or overly complex `.proto` files (e.g., cyclic dependencies, excessively deep message nesting, or invalid import paths), causing the Rust code generator to output uncompilable code with lifetime issues and stack overflows.

We used to rely on a legacy C++ utility to filter these files, which is available as a stripped binary at `/app/legacy_filter`. However, we are moving away from it and need a robust Bash script to replace its functionality. 

Your task is to write a Bash script at `/home/user/proto_filter.sh` that takes a single argument (the path to a `.proto` file) and validates it. It should exit with code `0` if the file is safe to compile (clean), and exit with code `1` (or any non-zero) if the file violates our safety rules (evil).

By analyzing `/app/legacy_filter` (you can run it against various files or inspect its strings), you should deduce the three strict rules it enforces regarding:
1. Permitted `import` statement paths (path traversal prevention).
2. Maximum allowed depth of nested `message` declarations (graph traversal depth limit).
3. Restricted gRPC service names.

Implement these exact rules in `/home/user/proto_filter.sh` using Bash. Ensure your script is executable (`chmod +x`). Our CI system will test your script against a hidden corpus of clean and malicious `.proto` files to ensure it blocks 100% of the bad files while allowing 100% of the good ones.