You are acting as a configuration manager tracking differential changes across server environments.

You have an archive of previous configurations located at `/home/user/configs_old.tar.gz`.
You also have a directory containing the current, active configurations located at `/home/user/configs_current/`.

Your task is to:
1. Identify which configuration files in `/home/user/configs_current/` differ from their counterparts in the old archive.
2. For only the files in `/home/user/configs_current/` that have changed, perform an in-place text edit to update deprecated keys:
   - Replace all occurrences of `DEBUG_LEVEL=1` with `LOG_LEVEL=debug`
   - Replace all occurrences of `SERVER_PORT=8080` with `SERVER_PORT=9000`
3. Create a bzip2-compressed tarball containing ONLY these updated (differing) files from the `configs_current` directory. Save this patch archive to `/home/user/configs_patch.tar.bz2`. The archive should contain the files at the root level (e.g., `web.conf`, not `configs_current/web.conf`).
4. Create a text file at `/home/user/patch_log.txt` containing the exact basenames of the files you modified and archived, with one filename per line, sorted alphabetically.

Ensure you only use standard bash built-ins and coreutils for this task. Do not modify the original old archive.