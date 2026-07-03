You are an artifact manager responsible for curating a software repository located in `/home/user/artifacts`. Due to a recent messy migration, the repository contains duplicate binaries and misconfigured text files.

Your goal is to clean up the repository, generate a new checksum manifest, and package a release archive.

In `/home/user/artifacts/inventory.txt`, you will find a pipe-separated list of tracked files. The format is:
`filename|filetype|status`

Perform the following operations exclusively using Bash shell built-ins and standard CLI tools:

1. **Deduplicate Binaries:**
   - Find all files marked as `binary` in the inventory.
   - Calculate their SHA256 checksums.
   - If there are files with identical content (same checksum), keep ONLY the one whose filename comes first alphabetically. Delete the other duplicate files from the `/home/user/artifacts` directory.

2. **Fix Text Configurations:**
   - Find all files marked as `text` that also have the status `active` in the inventory.
   - For these files, replace all instances of the string `DEV_SERVER` with `PROD_SERVER`.
   - Do not modify text files with the `archived` status.

3. **Generate a New Manifest:**
   - Generate a checksum file at `/home/user/checksums.txt`.
   - It must contain the `sha256sum` output for ALL remaining files in `/home/user/artifacts/` (excluding `inventory.txt`), sorted alphabetically by filename.
   - The format should be the standard `sha256sum` output (e.g., `<hash>  <filename>`).

4. **Package the Release:**
   - Create a compressed tarball at `/home/user/release.tar.gz`.
   - The tarball must contain ONLY the remaining files that have the status `active` in the inventory.
   - Do NOT include `inventory.txt` in the tarball.
   - The files in the tarball should not contain absolute paths (i.e., they should be at the root of the archive or inside an `artifacts/` folder, depending on how you tar them, but do not use full paths like `/home/user/artifacts/...`).

Ensure you have completed all steps accurately. The automated tests will verify the existence of the correct files, their exact contents, and the contents of the archive.