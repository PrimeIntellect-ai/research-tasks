You are an artifact manager responsible for curating an incoming binary repository. We have received an incoming archive at `/home/user/incoming/payload.zip` which we suspect might be a malicious "zip slip" payload containing paths designed to escape the extraction directory.

Your task is to write and execute a Python script that safely processes this archive without automatically extracting it using standard insecure tools. 

Here are the requirements:
1. Parse `/home/user/incoming/payload.zip` using Python.
2. Analyze the paths of all files in the archive. A path is considered "malicious" if, when resolved against a base directory, it would escape that base directory (e.g., contains `../` components that traverse above the root).
3. Log the exact archive paths of all malicious entries to `/home/user/artifacts/malicious.log`. Each malicious path must be on a new line. Sort the lines alphabetically.
4. For all "safe" entries (those that do not escape the base directory):
   - Extract their binary content.
   - Save them into `/home/user/artifacts/raw/` using their original basename (ignoring any original directory structure within the zip), but append `.safe` to the filename. For example, `configs/settings.dat` becomes `/home/user/artifacts/raw/settings.dat.safe`.
   - Create a symbolic link in `/home/user/artifacts/links/` that uses the original basename (e.g., `settings.dat`) which points to the absolute path of the newly renamed `.safe` file in the `raw` directory.

Directories `/home/user/artifacts/raw/` and `/home/user/artifacts/links/` have already been created for you. Ignore directory entries in the zip file (only process files). You should write a Python script to accomplish this and run it.