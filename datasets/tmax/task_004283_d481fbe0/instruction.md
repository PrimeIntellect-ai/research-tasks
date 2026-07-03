You are a backup administrator responsible for archiving application logs. You have a mix of old archives and active log directories, some of which contain sensitive information and symbolic links that should not be archived directly.

Your task is to consolidate these files into a single, sanitized archive.

Here are the requirements:
1. Directory Setup:
   - Active logs are located in `/home/user/data/logs/`.
   - Old archives are located in `/home/user/archive/`.
   - Create a temporary working directory at `/home/user/staging/`.

2. Process Old Archives:
   - Check all `.tar.gz` files in `/home/user/archive/`. 
   - Verify their integrity. Extract only the valid, uncorrupted archives into `/home/user/staging/`. Ignore any corrupted archives.

3. Process Active Logs:
   - Find all `.log` files in `/home/user/data/logs/`.
   - You MUST ignore any symbolic links (only process regular files).
   - For each regular log file, sanitize the contents by replacing every occurrence of the exact word `SECRET` with `REDACTED`.
   - Place the sanitized log files into `/home/user/staging/`, preserving their original filenames.

4. Create Final Archive:
   - Create a new archive at `/home/user/final_backup.tar.gz` containing all the files in `/home/user/staging/`.
   - The files should be at the root of the archive (do not include the `/home/user/staging/` directory structure itself in the archive).

Ensure you use Bash commands and tools like `sed`, `find`, `tar`, and `gzip` to accomplish this.