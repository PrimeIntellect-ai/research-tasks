You are tasked with building a Go utility to process and analyze historical configuration backups for a configuration manager.

We have a set of backup archives in the directory `/home/user/config_backups`. 
Some are standard tarballs (`.tar.gz`), and some use a custom proprietary format (`.clog`).
A `.clog` file is simply a standard `.tar.gz` file that has been fully base64-encoded.

Inside `/home/user/config_backups`, there is also a file named `checksums.txt` containing the expected SHA256 checksums of all the archives. The format is standard `sha256sum` output: `<checksum>  <filename>`.

Your objective is to write and run a Go program at `/home/user/analyzer.go` that does the following:
1. Navigations and Integrity: Read `checksums.txt` and verify the SHA256 checksum of every `.tar.gz` and `.clog` file in the directory. If an archive's checksum does not match the one in `checksums.txt`, you must skip it entirely.
2. Custom Decompression & Extraction: For each valid archive, extract its contents in memory or to a temporary directory. If it's a `.clog` file, you must base64-decode it before treating it as a `.tar.gz`.
3. Multi-line Log Parsing: Inside each valid archive, there is exactly one file named `changes.log`. This file contains multi-line log records formatted exactly like this:
   ```
   START_CHANGE
   Author: <AuthorName>
   Date: <YYYY-MM-DD>
   Files: <Number>
   Details:
   <Line 1 of details>
   <Line 2 of details>
   ...
   END_CHANGE
   ```
   (There may be multiple blank lines or other text between records, but a record always strictly begins with `START_CHANGE` and ends with `END_CHANGE`).
4. Aggregation: Count the total number of changes authored by each person across all valid archives.
5. Output: Write the final aggregated counts to `/home/user/summary.json` as a single JSON object where the keys are the Author names and the values are the integer counts. Example:
   ```json
   {
     "Alice": 5,
     "Bob": 1
   }
   ```

Write your Go code, execute it to generate the `/home/user/summary.json` file, and ensure it correctly reflects the data from the valid archives.