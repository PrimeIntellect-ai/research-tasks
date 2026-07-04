You are a platform engineer responsible for securing and maintaining a custom CI/CD build system. Our pipelines process custom `.build` files, which declare dependencies and cross-compilation instructions.

Your task consists of three parts:

1. **Information Extraction**:
   We have a diagram of our build architecture at `/app/architecture.png`. Use OCR (e.g., `tesseract`) to extract the text from this image. Find the string formatted as `Pipeline-ID: <alphanumeric_string>` and save just the alphanumeric string to `/home/user/pipeline_id.txt`.

2. **Build Configuration Linter (Sanitiser)**:
   You must write a Bash script `/home/user/linter.sh` that takes a path to a `.build` file as its first argument. 
   The script must act as a security linter, exiting with `0` if the file is safe, and `1` if it is malicious.
   Our `.build` files are text files where each line is a key-value pair separated by a space (e.g., `COMMAND gcc src.c`, `FLAGS -target x86_64-linux-gnu`).
   A file is considered **malicious** (evil) if ANY of the following are true:
   - The `COMMAND` line contains the words `curl`, `wget`, or `nc`.
   - The `FLAGS` line contains an absolute path starting with `/` or relative paths containing `..` (which might be used to write cross-compiled binaries outside the allowed workspace).
   - The file contains an `EVAL` key (which evaluates arbitrary expressions).
   If none of these are present, the file is **clean**.

3. **Dependency Graph API**:
   Write a Bash script `/home/user/api.sh` that starts a simple HTTP REST API server on port `8080` (you may use `socat` or `nc`). 
   When it receives an HTTP `GET /dependencies` request, it should:
   - Parse all `.build` files in `/app/corpus/clean/`.
   - Each file has a `TARGET <name>` and an optional `DEPENDS <name1>,<name2>` line.
   - Return a valid JSON response containing the dependency graph mapping each target to its list of dependencies. For example: `{"app": ["lib1", "lib2"], "lib1": []}`.
   - Respond with HTTP 200 OK and the appropriate `Content-Type`.

Make sure all your scripts are executable. Do not start the API server in the background permanently; we will test your scripts individually.