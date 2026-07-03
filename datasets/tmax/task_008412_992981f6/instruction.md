You are acting as a security-focused release engineer. We have a configuration manager application that processes configuration updates delivered as zip archives. 

There is a vulnerable Go script at `/home/user/extract.go` designed to extract `/home/user/update.zip` into the `/home/user/configs/` directory. However, we have detected that some uploaded archives contain crafted file paths (e.g., `../../...`) intended to exploit a "Zip Slip" directory traversal vulnerability and overwrite sensitive files outside the target directory.

Your task consists of three steps:
1. Modify `/home/user/extract.go` to patch the Zip Slip vulnerability. Ensure that any file in the archive whose resolved destination path falls outside of the absolute path of `/home/user/configs/` is completely skipped. (Only extract files that safely resolve inside the target directory).
2. Execute the Go script to extract `/home/user/update.zip` into the `/home/user/configs/` directory. Create the directory if it does not exist.
3. Generate a SHA-256 manifest of the safely extracted files to verify the integrity of the configuration. Create a file at `/home/user/manifest.txt` containing the checksums. To do this, navigate into `/home/user/configs/` and run `sha256sum` on all extracted files (output format should match the default `sha256sum *` format, e.g., `<hash>  filename`). Sort the manifest alphabetically by filename.

Constraints:
- Do not manually extract the zip file using the `unzip` CLI. You must fix and use the provided Go program.
- Ensure the Go program compiles and runs cleanly.