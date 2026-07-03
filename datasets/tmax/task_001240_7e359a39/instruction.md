You are tasked with building a configuration tracking log parser in Rust that enforces strict path sanitization. Our configuration manager reads operations from a Write-Ahead Log (WAL), including extracting files from archived packages. We need a robust filter to prevent "Zip Slip" vulnerabilities where maliciously crafted archive paths overwrite files outside the intended target directory.

First, inspect the scanned company policy document located at `/app/scan_policy.png`. You will need to extract the "Mandatory Asset Prefix" from this image (e.g., using Tesseract OCR). You must prepend this exact prefix to all successfully sanitized configuration file names to conform to our bulk-renaming rules.

Write a Rust program. You can initialize it at `/home/user/log_sanitizer/`. 
The program must be compiled to an executable at `/home/user/log_sanitizer/target/release/sanitizer`.

The program must read a text-based WAL line-by-line from `stdin` until EOF. Each line has the format:
`<SEQ_ID> <OPERATION> <RAW_PATH>`
(Components are separated by a single space. `SEQ_ID` is an integer. `OPERATION` is either `EXTRACT` or `REMOVE`.)

Your program must securely evaluate `RAW_PATH` as if it were being extracted into a hypothetical base directory `/config_root/`. 
1. Normalize the path (resolve `.` and `..` components). 
2. If the normalized path attempts to escape `/config_root/` (i.e., a Zip Slip attempt), the program must immediately print to `stdout`: `<SEQ_ID> REJECT`.
3. If the normalized path securely resides within `/config_root/` (or its subdirectories), format the final relative path by extracting the final file name, prepending the "Mandatory Asset Prefix" (extracted from the image), and rejoining it to the normalized directory structure. Print to `stdout`: `<SEQ_ID> ACCEPT <NORMALIZED_RELATIVE_DIR>/<PREFIX><FILENAME>` (or just `<PREFIX><FILENAME>` if it's at the root).
4. If the line is malformed, ignore it.

For example, if the prefix from the image is `SECURE_`, and the WAL line is `101 EXTRACT ../config_root/db/../db/main.conf`, the resolved path is `/config_root/db/main.conf`. This is valid. You should output `101 ACCEPT db/SECURE_main.conf`.
If the WAL line is `102 EXTRACT foo/../../etc/shadow`, it escapes the root. Output `102 REJECT`.

Write, test, and compile your Rust code. The final output must be highly performant, handling thousands of lines correctly to ensure archive integrity and security.