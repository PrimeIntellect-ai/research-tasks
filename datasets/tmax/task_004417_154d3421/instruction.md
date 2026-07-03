You are a platform engineer maintaining a legacy CI/CD pipeline. Recently, the pipeline has been failing because malicious dependency manifests (similar to node peer dependency conflicts) have been injected into the system. 

We need to build a robust Python-based filter (`/home/user/pipeline_guard.py`) to validate these manifests before they enter the build system.

You are provided with:
1. `/home/user/libcert.so`: A compiled C library used for legacy signature verification.
2. `/app/legacy_docs.png`: A scanned snippet of the original pipeline documentation.

Your task:
1. Extract the text from `/app/legacy_docs.png` (using `tesseract` or similar tools). This image contains critical information: the exact C function signature exported by `libcert.so` and the exact peer-dependency security rules you must enforce.
2. Create a Protobuf schema file `/home/user/manifest.proto` with the following structure:
   - `package_name` (string, tag 1)
   - `version` (string, tag 2)
   - `peer_deps` (repeated string, tag 3)
   - `is_signed` (bool, tag 4)
3. Compile the Protobuf schema for Python.
4. Write a CLI tool at `/home/user/pipeline_guard.py` that takes a single file path as an argument. The file will be a binary-encoded protobuf `Manifest`.
5. The script must deserialize the manifest, and decide whether to ACCEPT or REJECT it based on:
   a) The security rules extracted from the image.
   b) A call to the C library via Python's `ctypes` (FFI). The extracted documentation in the image specifies the function signature. You must pass the `package_name` and `version` to this C function.
6. The script should exit with code 0 if the manifest is ACCEPTED, and exit with code 1 if the manifest is REJECTED. It can print anything to stdout/stderr.

You can test your script against the manifest files located in `/home/user/test_manifests/`. Make sure your `pipeline_guard.py` script is executable and works correctly.