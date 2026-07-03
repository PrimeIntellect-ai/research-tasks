You are an AI assistant helping a backup operator test and validate a staging environment for system restores.

Your task consists of two parts: setting up the restored directory structure using an idempotent script, and writing a Go-based path validation tool to verify ACL rules against an oracle.

**Part 1: Staged Restore Directory Setup**
Write an idempotent bash script at `/home/user/setup_restore.sh` that sets up a rolling deployment structure for restored backups:
1. Create the base directory `/home/user/backup_staging/`.
2. Create two directories for staged restores: `/home/user/backup_staging/releases/v1` and `/home/user/backup_staging/releases/v2`.
3. Set the permissions of the `releases` directory to `0755`.
4. Set the permissions of `v1` and `v2` to `0700`.
5. Create a symlink at `/home/user/backup_staging/current` that points to `/home/user/backup_staging/releases/v1`. If the symlink already exists, it should be updated to point to `v1`.
Ensure the script can be run multiple times safely without producing errors or creating nested symlinks.

**Part 2: Path Validator Tool**
As part of the restore validation, we need a custom path and ACL evaluator written in Go.
An image containing a critical secret key has been recovered and is available at `/app/restore_secret.png`. The image contains text in the format `SECRET_KEY: <value>`. You need to extract this `<value>`.

Write a Go program at `/home/user/path_validator.go` and compile it to an executable at `/home/user/path_validator`.
The program must take exactly one command-line argument: a file path.
It must output a single line based on the following rules:
1. Normalize the path using Go's `path.Clean`.
2. If the normalized path is exactly `/restricted` or starts with `/restricted/`, output: `ACL: 0600`
3. If the normalized path contains the exact string of the `<value>` extracted from the image, output: `ACL: 0777` (This rule takes precedence over rule 2 if both apply).
4. If neither rule applies, compute the MD5 hash of the normalized path (as a string). Output `ACL: 0644 HASH: ` followed by the first 4 characters of the lowercase hexadecimal MD5 hash.

Example: If the secret key is "DOG" and the input is `foo/bar/../DOG/baz`, the normalized path is `foo/DOG/baz`. It contains "DOG", so the output is `ACL: 0777`.

Your executable `/home/user/path_validator` will be tested against a hidden oracle using random inputs. It must produce bit-exact equivalent output to the oracle.