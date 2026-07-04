You are tasked with building a robust configuration backup tool in Go. We have a set of application configurations in `/home/user/config_manager/data/` that need to be backed up, but the directory structure is notoriously messy and contains infinite symlink loops.

Write a Go program at `/home/user/backup_tool.go` and compile it to `/home/user/backup_tool`. The program must perform the following tasks:

1. **File Locking**: Before running, the program must acquire an exclusive file lock on `/home/user/backup.lock` to prevent concurrent executions. If it cannot acquire the lock, it should exit with a non-zero status.
2. **Manifest Parsing**: Read a JSON manifest located at `/home/user/config_manager/manifest.json`. The manifest has the following structure:
   ```json
   {
     "targets": [
       "/home/user/config_manager/data"
     ]
   }
   ```
3. **Directory Traversal & Loop Avoidance**: For each target directory in the manifest, recursively find all files. You must correctly handle symbolic links. To prevent infinite loops caused by cyclic symlinks, you must track visited paths or inodes and skip any symlink that points to an already visited directory in the current traversal path.
4. **Data Transformation (Redaction)**: As you read `.csv` files, you must apply a large-scale text transformation. Look for any instances of `SECRET_KEY=<alphanumeric_string>` (e.g., `SECRET_KEY=ABC123xyz`) and replace them with `SECRET_KEY=REDACTED`.
5. **Archive Creation**: Package the discovered (and transformed) files into a single gzip-compressed tarball at `/home/user/backup_archive.tar.gz`. The internal paths in the tarball should be relative to `/home/user/config_manager/data` (e.g., a file at `/home/user/config_manager/data/app/config.csv` should appear as `app/config.csv` inside the archive). 

Execute your Go program so that `/home/user/backup_archive.tar.gz` is successfully generated.