You are acting as a storage administrator managing disk space for a complex set of user directories. 

We have a recurrent issue where users create complex symlink structures, sometimes resulting in infinite loops (e.g., a symlink inside a directory pointing back to its parent). Standard backup scripts keep crashing or running out of memory when they follow these symlinks. 

Your task is to write a custom, robust incremental backup tool in Rust that can safely navigate these structures.

Here are the requirements:

1. **Setup**: Create a new Rust binary project at `/workspace/safe_backup`. You can use any standard crates you need (like `serde`, `serde_json`, `walkdir`, etc.).

2. **Configuration**: Your tool must accept a single command-line argument: the path to a JSON configuration file. 
   The config file will be located at `/workspace/backup_config.json` and will have the following structure:
   ```json
   {
     "sources": ["/workspace/data"],
     "destination": "/workspace/backup",
     "last_backup_time": 1700000000
   }
   ```
   *Note: I have already created `/workspace/backup_config.json` and the `/workspace/data` directory with test data, including symlink loops.*

3. **Incremental Backup Logic**:
   - The tool must traverse all directories listed in the `sources` array.
   - It must copy regular files to the `destination` directory, preserving the directory structure relative to the source directory. For example, `/workspace/data/dirA/file.txt` should be copied to `/workspace/backup/dirA/file.txt`.
   - **Important**: It should ONLY copy files whose UNIX modification timestamp (in seconds) is strictly greater than `last_backup_time`.

4. **Symlink Handling & Path Manipulation**:
   - The tool MUST follow symlinks. If a symlink points to a file, copy the file (if it meets the time constraint) to the destination under the symlink's name.
   - If a symlink points to a directory, traverse into it as if it were a normal directory.
   - **Loop Detection**: To prevent infinite loops, your tool must track the canonicalized absolute paths of the directories it is currently traversing. If following a symlink leads to a directory that is already in the current traversal stack (an ancestor), it MUST abort that specific branch.
   - When an infinite loop is detected, the tool must append exactly this line to `/workspace/backup.log`:
     `LOOP DETECTED: <path_to_symlink>`
     (Replace `<path_to_symlink>` with the absolute path of the symlink that caused the loop, e.g., `LOOP DETECTED: /workspace/data/dirA/loop_link`).

5. **Execution**: Once written, compile and run your tool using the provided `/workspace/backup_config.json`. Ensure `/workspace/backup` and `/workspace/backup.log` are correctly populated.

Ensure your code is compiled in release or debug mode and executed successfully before completing the task.