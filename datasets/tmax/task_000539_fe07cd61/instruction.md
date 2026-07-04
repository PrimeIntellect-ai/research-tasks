You are tasked with building an artifact transformation pipeline to curate a messy set of binary repositories. As an artifact manager, you need to flatten the incoming files into a content-addressable storage pool, and then reconstruct a curated, hierarchical virtual repository using symbolic links based on provided metadata. Finally, you must generate a verification manifest using standard Linux tools and stream redirections.

**Initial State:**
You have a directory at `/home/user/incoming/` containing several binary artifacts scattered across subdirectories, along with a metadata file at `/home/user/incoming/metadata.csv`.

The `metadata.csv` file has the following format (without a header):
`relative_file_path,os_target,version`
Example line: `projA/mac/release.zip,macos,1.0.0`

**Your Objectives:**

1. **Create the Content-Addressable Pool:**
   Create a directory at `/home/user/artifact_pool/`.
   For every artifact listed in the `metadata.csv`, calculate its SHA-256 hash.
   Copy the artifact into `/home/user/artifact_pool/` and rename it to exactly its SHA-256 hash, preserving its original file extension. 
   *(Example: if `release.zip` has hash `abc...123`, the new file must be `/home/user/artifact_pool/abc...123.zip`)*

2. **Construct the Curated Virtual Repository (Path Manipulation):**
   Create a directory at `/home/user/curated_repo/`.
   Using the metadata, recreate a clean directory structure: `/home/user/curated_repo/<os_target>/<version>/`.
   Inside each version directory, create a **symbolic link** named `artifact.<original_extension>` that points to the corresponding content-addressable file in `/home/user/artifact_pool/`.
   Make sure you use absolute paths for the symlink targets to ensure they resolve correctly.

3. **Generate the Final Manifest:**
   Using bash stream redirection and piping, generate a consolidated manifest file exactly at `/home/user/curated_repo/manifest.txt`.
   For each processed artifact, write exactly one line in the manifest with the following format:
   `<absolute_path_to_symlink>|<absolute_path_to_pool_file>|<sha256_hash>`
   
   The lines in `manifest.txt` **must be sorted alphabetically** by the `<absolute_path_to_symlink>`.

**Constraints:**
- Use standard shell commands and tools (bash, awk, sha256sum, etc.). No external scripts are provided.
- Ensure all directories are created with the necessary permissions for standard user access.
- Do not modify or delete the original files in `/home/user/incoming/`.