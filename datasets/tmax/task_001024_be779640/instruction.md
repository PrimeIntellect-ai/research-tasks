We are building a configuration manager that archives and tracks system configuration changes via tarballs. However, we need to ensure that user-submitted backup archives are safe to extract and comply with our latest mount policies. 

There is an image file located at `/app/policy.png` which contains a snippet of a memo. You will need to extract the text from this image to find the currently denied mount path (it will be listed as `DENY_MOUNT: <path>`).

Your task is to write a verification program at `/home/user/verify_backup.sh` that takes a single argument: the absolute path to a configuration tar archive (`.tar`). 

The script must evaluate the archive and exit with `0` if it is safe (clean), and exit with `1` if it violates any rules (evil). You can use any programming language, but the entry point must be an executable script at `/home/user/verify_backup.sh`.

An archive violates the rules and MUST be rejected (exit code `1`) if:
1. **Path Traversal / Tarbomb**: Any file or directory inside the tarball contains absolute paths (starting with `/`) or path traversal sequences (`../`) that attempt to escape the root of the archive.
2. **Absolute Symlinks**: Any symlink inside the tarball points to an absolute path.
3. **Policy Violation**: The archive contains a configuration file named `app_config.json` (at the root of the archive) which contains a `"mount_path"` key whose value matches or is a subdirectory of the denied mount path extracted from `/app/policy.png`.

If none of these violations occur, the script must accept the archive (exit code `0`).

Make sure your script does not accidentally execute or permanently extract malicious files outside of a secure temporary directory during its analysis.