You are tasked with building a bash-based configuration tracking workflow. A system's configuration files have evolved, and you need to determine exactly what changed since the last backup and package the updates.

You have been provided with a legacy backup of the configuration state. This backup is stored as a split, nested archive in `/home/user/backups/`:
- `legacy_backup.tar.gz.00`
- `legacy_backup.tar.gz.01`
- `legacy_backup.tar.gz.02`

When reassembled and extracted, this archive contains an inner archive named `internal_configs.tar`. Extracting `internal_configs.tar` will reveal the previous state of the configuration directory.

The current, live configuration state is located in `/home/user/current_configs/`. This directory contains various `.conf` files, subdirectories, and symlinks.

Your objective is to complete the following steps:
1. Reassemble and fully extract the legacy backup to `/home/user/legacy_extracted/`.
2. Recursively traverse both `/home/user/legacy_extracted/` and `/home/user/current_configs/`.
3. Compare the `.conf` files in the current state against the legacy state. Note: You must *follow* all symlinks in `/home/user/current_configs/` and evaluate the contents of the files they point to. If a symlink points to a file outside the tree, treat the target's content as the configuration data.
4. Identify all `.conf` files that are either `NEW` (do not exist in the legacy backup by path) or `MODIFIED` (exist but have different SHA256 checksums). Do not track deleted files.
5. Generate a manifest file at `/home/user/change_manifest.txt` with exactly the following format for each new or modified file, sorted alphabetically by the relative file path:
   `[STATUS] ./relative/path/to/file.conf [NEW_SHA256_CHECKSUM]`
   *(Example: `[MODIFIED] ./network/interfaces.conf e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`)*
6. Create a new compressed tarball at `/home/user/update.tar.gz` containing ONLY the `NEW` and `MODIFIED` files from `/home/user/current_configs/`. The internal structure of this archive should match their relative paths inside `current_configs` (e.g., `network/interfaces.conf`). Dereference (follow) symlinks so the actual file contents are archived, not the links themselves.

Ensure all paths in your manifest are strictly relative to `/home/user/current_configs/` (starting with `./`).