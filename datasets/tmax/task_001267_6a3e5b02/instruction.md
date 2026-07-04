You are an artifact manager responsible for curating a local binary repository. 

You have a repository located at `/home/user/artifacts/` containing several `.bin` files and a metadata manifest file named `manifest.json`. 

A recent security audit revealed that some of these compiled binaries contain a deprecated, hardcoded magic byte sequence that must be patched. Furthermore, the `manifest.json` checksums are outdated and need to be regenerated after the patch.

Your task is to:
1. Find all `.bin` files in `/home/user/artifacts/`.
2. Binary Patching: Search inside these `.bin` files for the exact hex byte sequence `DE AD BE EF 00 00` (6 bytes) and replace every occurrence in-place with the new sequence `CA FE BA BE 00 00`. You must not alter any other bytes in the files.
3. Compute the new SHA-256 checksums for all the `.bin` files.
4. Update the manifest: The file `/home/user/artifacts/manifest.json` contains a JSON structure with an `artifacts` array. Each object in the array has a `name` (the filename, e.g., "app1.bin") and a `sha256` key. Update the `sha256` values in this JSON file to reflect the new, patched hashes of the binaries. Do not change the overall structure of the JSON.
5. Create a summary file: Generate a CSV file at `/home/user/artifacts/summary.csv` containing the updated information. The CSV must have exactly this header: `artifact_name,new_sha256`. Add a row for each `.bin` file, sorted alphabetically by the `artifact_name`.

Please complete these steps using Bash shell commands and tools available on a standard Linux system (like `xxd`, `sed`, `awk`, `jq`, `sha256sum`, or `perl`).