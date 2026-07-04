You are an artifact manager responsible for curating a local binary repository. Upstream build systems dump various artifact archives into a staging directory at `/home/user/staging_repo`. Over time, some of these transfers fail, resulting in corrupted archives. Additionally, you only want to promote specific "fat binaries" to the final release repository.

Your task is to write and execute a Python script at `/home/user/curate_artifacts.py` that automates this curation pipeline.

The script must perform the following operations:
1. **Find and Verify**: Locate all `.zip` and `.tar.gz` files recursively within `/home/user/staging_repo`. Verify the structural integrity of each archive (e.g., ensure they can be read and are not corrupted).
2. **Log Corrupted Archives**: If an archive is corrupted or invalid, write its absolute file path to `/home/user/corrupted.log`. Each path should be on a new line, and the list must be sorted alphabetically.
3. **Extract Valid Archives**: Extract all files from the *valid* archives into a temporary directory at `/home/user/extracted_staging`.
4. **Metadata-Based Search**: Search through `/home/user/extracted_staging` (recursively) for target binaries. A target binary is defined as any file that:
   - Ends with the `.bin` extension.
   - Has a file size strictly greater than `100,000` bytes.
5. **Create Curated Release**: Create a new, gzip-compressed tarball at `/home/user/curated_release.tar.gz` containing only the target binaries identified in step 4. When adding these files to the new archive, flatten the directory structure (i.e., the `.bin` files should appear at the root level of the archive, without their parent directories).

Requirements:
- Do not use absolute paths from `/home/user/extracted_staging` inside the final `curated_release.tar.gz`.
- Ensure `/home/user/corrupted.log` strictly contains only the absolute paths of the failed archives.
- Execute your script to produce the final state.