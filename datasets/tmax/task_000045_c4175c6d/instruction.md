You are helping a backup administrator who is trying to archive a set of backup chunks. However, the legacy backup system sometimes creates chaotic directory structures containing infinite symlink loops, which causes standard archiving tools to crash or hang. 

Your task is to write a Go program that safely scans the directory `/home/user/backup_source`, identifies valid backup files, computes their checksums, and generates a manifest file, all while successfully avoiding any infinite symlink loops.

Here are the specific requirements for your Go program:
1. **Traverse the Directory:** Recursively scan `/home/user/backup_source`. You must follow symlinks to directories, but you must implement a mechanism to detect and prevent infinite loops (e.g., a symlink pointing to its own parent directory).
2. **Identify Valid Backup Files:** A valid backup chunk is a regular file (or a symlink to a regular file) where the first 4 bytes exactly match the binary signature `BKP\x01` (Hex: `42 4B 50 01`). You should ignore any files that do not start with these exact magic bytes, or files that are too short.
3. **Generate a Checksum:** For each valid backup file found, compute its SHA-256 checksum.
4. **Output a Manifest:** Create a JSON manifest file at `/home/user/backup_manifest.json` with the following exact structure. The `path` must be the absolute resolved path of the valid file. The list of files must be sorted alphabetically by the `path` string.

```json
{
  "files": [
    {
      "path": "/home/user/backup_source/chunk1.bin",
      "checksum": "a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e"
    },
    {
      "path": "/home/user/backup_source/subdir/chunk2.bin",
      "checksum": "..."
    }
  ]
}
```

Write the Go program, compile it, and run it to produce `/home/user/backup_manifest.json`.