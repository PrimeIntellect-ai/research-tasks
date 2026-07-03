You need to build a secure configuration deployment daemon in Python.

We have a system that receives configuration updates as tarballs (`.tar.gz`) in the `/home/user/incoming/` directory. Your task is to write a Python script at `/home/user/config_watcher.py` that processes any `.tar.gz` files currently in this directory, and securely deploys their contents.

Here is the exact workflow your script must follow for each `.tar.gz` file found in `/home/user/incoming/`:
1. **Secure Extraction**: Extract the archive into `/home/user/extracted/<archive_basename>/` (e.g., if the archive is `update1.tar.gz`, extract to `/home/user/extracted/update1/`).
   * **Security Requirement (Zip Slip Prevention)**: You must inspect each file in the tarball before extraction. If any file path in the archive attempts to traverse outside the target extraction directory (e.g., contains `../` or starts with `/`), you must **skip** extracting that specific file and write a line to `/home/user/configs/security.log` in the exact format: `REJECTED: <archive_filename> - <malicious_member_path>`.
2. **Configuration Interpretation**: Inside the extracted archive, there should be a `deploy.json` file. It contains a list of files to deploy, formatted as: `{"deploy": ["file1.conf", "dir/file2.conf"]}`.
3. **Deployment**: For each file listed in the `deploy.json` "deploy" array, copy it from the extracted directory to `/home/user/configs/`. (Do not preserve directory structures from the archive when copying to `/home/user/configs/`; flatten them, saving directly inside `/home/user/configs/`).
4. **Manifest Generation**: For every file successfully copied to `/home/user/configs/`, calculate its SHA-256 checksum and append it to `/home/user/configs/manifest.txt` in the format: `<sha256_hash>  <filename>`.
5. **Cleanup**: Delete the processed `.tar.gz` file from `/home/user/incoming/`.

The environment has already been pre-populated with some `.tar.gz` files in `/home/user/incoming/`.
Write the script, ensure you install any necessary dependencies, and run your script so that it processes all existing files in the incoming directory. The script can exit once all existing `.tar.gz` files are processed and deleted.