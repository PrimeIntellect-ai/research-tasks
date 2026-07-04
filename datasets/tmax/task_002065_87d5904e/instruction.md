You need to help organize a messy project workspace by parsing a deployment configuration file, but there is a catch: the configuration may contain malicious or malformed paths that try to write outside the designated workspace (similar to a zip-slip vulnerability).

Your task is to write and execute a script (in the language of your choice) to process the configuration and create the appropriate file links.

Here are the details:
1. **Directories**: 
   - Source files are located in `/home/user/project_dir/source_files/`.
   - All output files must be linked inside `/home/user/project_dir/organized_workspace/`.

2. **Configuration File**:
   - The configuration is a JSON file located at `/home/user/project_dir/deployment_manifest.json`.
   - It contains an array of objects. Each object has three keys:
     - `src`: The name of the file in the `source_files` directory.
     - `dest`: The target relative path where the link should be created, evaluated strictly relative to `/home/user/project_dir/organized_workspace/`.
     - `link_type`: Either `"symlink"` or `"hardlink"`.

3. **Validation Requirements (Path Traversal Protection)**:
   - You must evaluate the ultimate resolved absolute path of the `dest` field. 
   - If the resolved `dest` path points to any location *outside* or exactly equal to `/home/user/project_dir/organized_workspace/` (e.g., `../`, or traversing up and out), it is considered an invalid escape attempt.
   - **For valid paths**: Create the requested link (`symlink` or `hardlink`) from the source file to the destination path. If the destination's parent directories do not exist inside `organized_workspace/`, create them. Note: Symlinks should be created with absolute paths pointing to the source file.
   - **For invalid paths**: Do NOT create the link. Instead, append a line to a log file at `/home/user/project_dir/path_escapes.log` in the exact format: `Invalid path escape attempt: <dest>` (where `<dest>` is the exact string value of `dest` from the JSON).

Execute your solution so that the links are created and the log file is generated.