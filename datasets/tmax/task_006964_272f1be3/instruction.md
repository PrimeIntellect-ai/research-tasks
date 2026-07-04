I need your help organizing and backing up a messy project directory located at `/home/user/project_data`. Over time, a bunch of symbolic links were added to the directory. Some of these links are useful, but unfortunately, some developers accidentally created circular symbolic links that cause infinite loops when standard backup tools try to follow them.

Your task is to write a script in the language of your choice (e.g., Python, Bash, Ruby) to safely traverse the directory, generate a manifest of files, and create a clean archive.

Here are the specific requirements:

1. **Traverse and Resolve:** Traverse `/home/user/project_data`. Resolve symbolic links to their real paths. 
2. **Circular Link Detection:** You must detect circular symbolic links. If a symlink points to a path that eventually loops back to itself, it must be flagged.
3. **Generate a Manifest:** Create a JSON manifest file exactly at `/home/user/backup_manifest.json`. The JSON must have the following structure:
    * `"files"`: A dictionary where keys are the *real* paths of all unique regular files (relative to `/home/user/project_data`) and values are their SHA-256 checksums. Only include each physical file once, even if multiple non-circular symlinks point to it. Use the primary physical file's relative path as the key.
    * `"circular_links"`: A sorted list of the paths of all symbolic links (relative to `/home/user/project_data`) that are part of a circular loop.
4. **Create the Archive:** Create a gzip-compressed tar archive at `/home/user/project_backup.tar.gz`. This archive should contain ONLY the unique regular files found during traversal. The files inside the archive should be stored at their real relative paths (e.g., `src/main.txt`, not absolute paths). Do not include any symbolic links or directories as empty entries in the archive.

**Example Manifest Format:**
```json
{
  "files": {
    "src/config.txt": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "assets/data.bin": "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92"
  },
  "circular_links": [
    "links/loop1",
    "links/subdir/loop2"
  ]
}
```

Ensure your script handles errors gracefully and produces exactly the outputs requested.