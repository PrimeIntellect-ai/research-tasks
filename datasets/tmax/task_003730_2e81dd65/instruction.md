You are tasked with building a secure configuration management restoration tool in Python that prevents "Zip Slip" vulnerabilities and unsafe link extractions.

Configuration archives are regularly received from external nodes, and we need a way to extract them safely. Python's built-in `tarfile` module is vulnerable to path traversal attacks if `extractall()` is used without sanitizing archive members. 

Write a Python script at `/home/user/config_restorer.py` that safely extracts tar archives while strictly containing all files, directories, and links within the designated target directory.

Requirements for `/home/user/config_restorer.py`:
1. It must accept exactly three command-line arguments:
   `python3 /home/user/config_restorer.py <archive_path> <target_directory> <log_file>`
2. It must extract the contents of `<archive_path>` to `<target_directory>`. If `<target_directory>` does not exist, it should be created.
3. **Zip Slip Protection:** Before extracting any member (file, directory, or link), the script must verify that the absolute resolved path of the extracted member falls strictly within the absolute path of `<target_directory>`.
4. **Link Protection:** If a member is a symbolic link or a hard link, the tool must verify that the *target* of the link also resolves to a path strictly within `<target_directory>`. 
5. **Logging:** If any archive member violates the path boundaries (either its extraction path or its link target escapes the target directory), the script must **skip** extracting that specific member and append its exact member name (as stored in the tar file) to the `<log_file>`. Each skipped member name should be on a new line.

Once your script is ready, test it by running it against the provided malicious archive:
`python3 /home/user/config_restorer.py /home/user/updates.tar /home/user/config_root /home/user/security.log`

(Note: You can assume `/home/user/updates.tar` will be present in the environment before you run your script).

Ensure that your script processes text, binary files, directories, symlinks, and hardlinks correctly, relying purely on the standard Python library (e.g., `tarfile`, `os`, `pathlib`).