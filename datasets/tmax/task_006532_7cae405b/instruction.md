You are an Artifact Manager responsible for curating a newly ingested binary repository. The repository contains a mix of nested archive files, but the ingestion pipeline has flagged several issues: some archives are corrupted, some contain malicious symlink loops that crash naive backup scripts, and some contain files compressed with a legacy custom format.

Your task is to write a script or use command-line tools to safely process these artifacts and generate a final manifest. You can use any programming language or shell script you prefer, as long as it executes successfully in the terminal.

Here are the requirements:

1. **Repository Location**: The raw artifacts are located in `/home/user/artifacts`.
2. **Archive Processing**:
   - Find all `.tar` files in the repository.
   - Verify their integrity. Ignore and do not extract any corrupted or truncated `.tar` files.
   - Extract the valid `.tar` files into `/home/user/staging`.
3. **Symlink Loop Mitigation**:
   - The extracted contents may contain symlinks that point to parent directories, creating infinite loops. You must safely detect and remove ANY symlinks inside `/home/user/staging` after extraction.
4. **Custom Decompression**:
   - Inside the extracted contents, you will find files with the `.cst` extension.
   - These files use a custom "compression" which simply reverses the byte order of the file.
   - For every `.cst` file, reverse the bytes back to their original order, save the decoded file with a `.dec` extension in the exact same directory, and delete the original `.cst` file. (For example, `data.cst` becomes `data.dec`).
5. **Manifest Generation**:
   - Once all valid archives are extracted, symlinks are removed, and `.cst` files are decoded, generate a manifest of all remaining regular files in `/home/user/staging`.
   - The manifest must be saved to `/home/user/manifest.txt`.
   - Each line of the manifest should be formatted exactly as the output of the `md5sum` command executed from within `/home/user/staging`:
     `<MD5_HASH>  <RELATIVE_FILE_PATH>`
   - The manifest must be sorted alphabetically by the relative file path.

Ensure your solution handles the entire pipeline and correctly outputs `/home/user/manifest.txt`.