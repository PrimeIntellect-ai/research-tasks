You are a FinOps analyst tasked with enforcing strict cloud storage cost policies using Git hooks and VM image introspection. 

Your team tracks infrastructure provisioning in a bare Git repository located at `/home/user/infra.git`. Each virtual machine configuration is stored as a JSON file. To prevent developers from provisioning oversized and unoptimized virtual machine images, you need to implement a server-side Git hook.

VM disk images are stored locally in `/home/user/storage/` as `.qcow2` files.

Write a Git `pre-receive` hook in **Python 3** at `/home/user/infra.git/hooks/pre-receive`. The hook must do the following:

1. Read the standard input provided by Git to a `pre-receive` hook (`<old-value> <new-value> <ref-name>`).
2. Identify all `.json` files that are being added or modified in the incoming push.
3. Parse the JSON files. Each JSON file contains a key `"image_path"` which points to an absolute file path of a `.qcow2` image in the storage directory.
4. For each image path, use the `qemu-img info` command (or inspect the filesystem) to determine its *actual* size on disk (the physical space it consumes, not its virtual capacity).
5. If any referenced image has an actual disk size strictly greater than `104857600` bytes (100 MB), the hook must:
   - Block the push (exit with a non-zero status).
   - Print a message to stdout: `FinOps Policy Violation: Image <image_path> is too large.`
   - Append a strict log entry to `/home/user/finops_alerts.log` in the exact format: `[REJECTED] <commit_hash> attempted to provision <image_path>` (use the `<new-value>` commit hash).
6. If all images are 100 MB or smaller, allow the push (exit with 0).

**Requirements & Environment:**
- Ensure your hook is executable.
- Do not modify the existing bare repository setup other than adding the hook.
- You can test your hook by cloning `/home/user/infra.git` to another directory, committing a JSON file, and pushing it back.
- You do not need root access. Do not use `sudo`. All operations should happen within `/home/user/`.

Write the hook so that it efficiently parses Git objects using `git cat-file` or `git show` to read the incoming JSON contents before they are committed to the main tree.