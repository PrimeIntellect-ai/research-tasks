You need to create a custom configuration tracking tool in Go. We have a mock configuration directory at `/home/user/etc_mock` containing various files. 

Your task is to write a Go program at `/home/user/config_manager.go` that takes a single command-line argument representing a snapshot name (e.g., `snapshot_01`). When run, the program must perform the following operations:

1. **Metadata-based File Search:** Scan `/home/user/etc_mock` and all its subdirectories for files ending in `.conf` that have been modified within the last 24 hours.
2. **Hard Link Management:** For every file found in step 1, create a hard link inside a new directory located at `/home/user/snapshots/<snapshot_name>`. To avoid filename collisions from subdirectories, flatten the names by replacing slashes with underscores (e.g., `/home/user/etc_mock/nginx/site.conf` becomes `/home/user/snapshots/<snapshot_name>/nginx_site.conf`). Strip the `/home/user/etc_mock/` prefix before flattening.
3. **Manifest and Checksum Generation:** Calculate the SHA256 checksum of each found file.
4. **Atomic Writes:** Write a JSON manifest to `/home/user/snapshots/<snapshot_name>/manifest.json` **atomically** (you must write to a temporary file in the same directory first, then rename it to `manifest.json`). The JSON should be a simple key-value map where the key is the original full path of the file, and the value is the lowercase hex string of the SHA256 checksum.
5. **Atomic Symbolic Link:** Atomically update a symbolic link at `/home/user/snapshots/current` to point to the newly created snapshot directory (`/home/user/snapshots/<snapshot_name>`). You must do this without leaving a window where `current` does not exist or points to nothing (e.g., create a temporary symlink and use rename/swap).

After writing the Go program, run it using: `go run /home/user/config_manager.go my_run`

**Output formatting for manifest.json:**
```json
{
  "/home/user/etc_mock/app1/db.conf": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  ...
}
```

Ensure your Go code strictly adheres to these requirements. You do not need to install any external dependencies; the Go standard library is sufficient.