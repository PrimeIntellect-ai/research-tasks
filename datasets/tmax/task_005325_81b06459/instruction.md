You are assisting a data researcher in organizing a large collection of dataset archives. The researcher uses a custom Go-based workflow to extract and index datasets. 

The researcher has provided a vendored Go package for archive handling located at `/app/vendored/archiver` (a localized version of a common archive utility). Recently, the researcher noticed that extracting some third-party datasets resulted in files being written outside the intended target directory. 

Your task consists of two parts:

1. **Fix the Vendored Package**: 
   Inspect the source code of the vendored package at `/app/vendored/archiver`. There is a deliberate perturbation (a missing security check) that allows path traversal during extraction (commonly known as a "zip slip" vulnerability). Fix the code in the vendored package so that any attempt to extract a file whose resolved path falls outside the destination directory results in an error being returned (specifically returning the standard `fmt.Errorf("illegal file path: %s", path)`).

2. **Create the Dataset Processor (`/home/user/process_datasets.go`)**:
   Write a Go program that utilizes the fixed `/app/vendored/archiver` package. The program must be compilable to `/home/user/process_datasets`.
   
   The program must accept exactly one argument: a path to a multi-line metadata log file.
   The metadata log contains multiline records formatted as follows:
   ```
   START_RECORD
   Archive: <path_to_zip_or_tar>
   Dataset-Type: <type>
   Description: <multi_line_description>
   ...
   END_RECORD
   ```
   
   For each record where `Dataset-Type` is exactly `verified_sensor_data`:
   - Use the fixed vendored archiver to extract the archive to a temporary directory. The archive may contain nested archives (e.g., a `.tar.gz` inside a `.zip`); you must recursively extract any nested archives found within the extracted files to the same temporary directory.
   - Perform a metadata-based search within the extracted directory: find all `.dat` files that have read permissions for the owner (`-r--------` or better) and are larger than 0 bytes.
   - Parse the `.dat` files and extract the first line of each valid `.dat` file.
   - Atomically write an index file named `dataset_index.jsonl` in `/home/user/output/`. The atomic write must ensure that partial data is never visible to concurrent readers (e.g., write to a temp file and rename). Each line in the JSONL should be `{"archive": "<Archive path>", "file": "<basename of .dat>", "header": "<first line content>"}`.

The automated verification will compile your program and fuzz-test it against hundreds of dynamically generated metadata logs and archives (some containing malicious zip-slip paths) to ensure it behaves identically to our reference implementation.