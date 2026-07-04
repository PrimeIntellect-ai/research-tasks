You are assisting a technical writer who receives documentation bundles from external contributors. These bundles are provided as ZIP archives. Recently, the team was warned about "Zip Slip" vulnerabilities, where improperly constructed archives contain file paths that resolve outside the intended extraction directory (e.g., using absolute paths or parent directory traversals like `../`).

Your task is to process a batch of incoming documentation archives located in `/home/user/docs_incoming/` using Python.

Please do the following:
1. Write a Python script to inspect all `.zip` files in `/home/user/docs_incoming/` without indiscriminately extracting them.
2. Check the internal file paths of each archive to detect Zip Slip vulnerabilities. An archive is considered malicious if ANY file inside it:
   - Starts with a forward slash `/` or backslash `\`.
   - Contains `../` or `..\` anywhere in its path.
3. Extract the contents of all **safe** archives into the directory `/home/user/docs_safe/` (create this directory if it does not exist).
4. Create a new, single consolidated archive at `/home/user/safe_docs_bundle.zip` containing all the extracted files from `/home/user/docs_safe/`. The files should be at the root of the zip (do not include the `docs_safe` folder itself in the archive paths).
5. Write the filenames (just the base names, e.g., `archive.zip`) of the malicious archives to a log file at `/home/user/malicious_zips.log`. The filenames must be sorted alphabetically, one per line.

Do not use external libraries outside the Python standard library.