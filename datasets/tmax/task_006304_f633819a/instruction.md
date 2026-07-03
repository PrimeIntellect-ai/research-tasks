You are a build engineer responsible for securing the artifacts of a web server application. The application dynamically loads several shared libraries, and a recent security bulletin has indicated that any library with a semantic version older than `1.5.0` might expose a vulnerable ABI symbol `insecure_legacy_auth` that allows authentication bypass.

Your task is to write a Python script at `/home/user/check_libs.py` to automate the auditing of these artifacts. 

The application artifacts are stored in `/home/user/artifacts/`. Inside this directory, there is a Base64-encoded file named `manifest.b64`. This file contains the inventory of the shared libraries in the format `filename:version`, separated by newlines.

Your script must perform the following actions:
1. Read and decode the `manifest.b64` file into a UTF-8 string.
2. Parse the filenames and their corresponding semantic versions.
3. Use PEP 440 semantic version comparison (e.g., using `packaging.version`) to identify libraries with a version strictly less than `1.5.0`.
4. For only the libraries identified as outdated in step 3, inspect the actual `.so` files located in `/home/user/artifacts/` to see if they export the vulnerable ABI symbol. You should use a system tool like `nm -D` to check if the exact symbol `insecure_legacy_auth` is exported (indicated by the `T` flag in `nm`, or just being present in the dynamic symbol table as a defined function).
5. Write an audit report to `/home/user/security_report.json` with the following strict JSON schema:
```json
{
  "outdated_libs": [
    "list",
    "of",
    "outdated",
    "filenames",
    "sorted",
    "alphabetically"
  ],
  "insecure_exports": [
    "list",
    "of",
    "filenames",
    "exporting",
    "the",
    "symbol",
    "sorted",
    "alphabetically"
  ]
}
```

Ensure your Python script executes successfully, handles the decoding properly, correctly compares the semantic versions, and accurately identifies the exported symbols from the shared objects. Run your script to generate the `/home/user/security_report.json` file.