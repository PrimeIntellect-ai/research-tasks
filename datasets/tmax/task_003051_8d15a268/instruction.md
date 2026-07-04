As a backup administrator, you need to recover data from a set of nested, potentially compromised archives. 

First, locate the image file `/app/recovery_instructions.png`. This image contains a handwritten note specifying the absolute path of the target directory where the recovered files must be placed.

We have received a historical backup archive at `/app/sample_backup.tar.gz`. This archive contains several nested `.zip` files. We suspect that some of these nested archives were tampered with and contain "Zip Slip" payloads—file entries designed to overwrite system files outside the target extraction directory by using path traversal (e.g., `../` or absolute paths).

Your task is to write a Python script at `/home/user/safe_extractor.py` that safely extracts nested archives. 
The script must accept exactly two command-line arguments:
1. The path to an input `.tar.gz` file (which contains nested `.zip` files).
2. The path to the output directory.

The script must:
- Extract the contents of the nested `.zip` files into the specified output directory.
- Silently skip any file entries inside the `.zip` files that would resolve to a path outside the output directory (preventing Zip Slip).
- Properly handle compressed streams and verify archive integrity where possible.

Once your script is ready, execute it against `/app/sample_backup.tar.gz` using the target directory you discovered from the image. 

Ensure your script is robust, as it will be evaluated on a hidden test archive to measure its extraction accuracy and security against path traversal attacks.