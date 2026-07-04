You are an artifact manager responsible for curating a newly ingested repository of binary files. 

You have been provided with an archive located at `/home/user/artifacts/raw_binaries.tar.gz`. 

Your task involves the following steps:
1. Extract the contents of `/home/user/artifacts/raw_binaries.tar.gz` into a new directory at `/home/user/artifacts/extracted`.
2. Inside the extracted archive, you will find a file named `metadata.json` and several raw binary files named with internal identifiers (e.g., `bin_1.dat`). The JSON file contains a list of objects with the keys `id`, `target_name`, and `expected_sha256`.
3. Rename all the raw binary files in the `extracted` directory from their `id` to their corresponding `target_name`.
4. Write a Go program at `/home/user/artifacts/verify.go`. This program must:
   - Read `/home/user/artifacts/extracted/metadata.json`.
   - Iterate through each entry.
   - Calculate the actual SHA-256 checksum of the renamed binary file located in the `/home/user/artifacts/extracted/` directory.
   - Compare the actual checksum against the `expected_sha256` value.
   - Generate a CSV report at `/home/user/artifacts/report.csv`.
5. The output CSV `/home/user/artifacts/report.csv` must have the exact following header and format:
   ```csv
   TargetName,Match
   <target_name_1>,<true_or_false>
   <target_name_2>,<true_or_false>
   ...
   ```
   (where Match is the boolean `true` if the hashes match, and `false` otherwise).
6. Run your Go program to generate the report. Ensure your code is thoroughly commented and correctly checks file integrity.