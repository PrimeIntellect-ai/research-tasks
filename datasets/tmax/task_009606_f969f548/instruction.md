You are an AI assistant helping a DevOps engineer curate a repository of binary artifacts. We have a set of legacy binary dumps that contain embedded configuration data in a specific text encoding. 

Your task is to write a Python script (and use any standard bash commands) to extract these configurations and package them. 

Here are the requirements:
1. Parse the configuration file located at `/home/user/curation_rules.ini`. It has the following structure:
   ```ini
   [Target]
   directory = /home/user/artifacts
   extension = .blob
   min_size_bytes = 1000
   ```
2. Search the specified `directory` for files matching the `extension` that are strictly greater than or equal to `min_size_bytes` in size.
3. For each matching file, open it and use memory-mapped I/O (`mmap`) to locate the embedded configuration block. The block starts immediately after the byte sequence `b'--CONFIG_START--'` and ends immediately before the byte sequence `b'--CONFIG_END--'`.
4. The bytes between these markers are encoded in UTF-16LE. You must extract these bytes and decode them into a standard UTF-8 string.
5. Create a directory called `/home/user/extracted/`. For every file from which you successfully extracted a configuration, save the UTF-8 string into a new file in this directory. The new file should have the same base name as the original artifact but with a `.conf` extension (e.g., `extracted/app1.conf`).
6. Finally, create a compressed tarball archive of the `extracted/` directory at `/home/user/curated_configs.tar.gz`. The tarball should contain the `extracted/` directory at its root (so extracting it creates the `extracted/` folder).

Ensure all paths in your code use the absolute paths provided.