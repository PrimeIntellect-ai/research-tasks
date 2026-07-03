You are acting as a technical writer organizing a documentation handover. You have received a compressed archive of documentation at `/home/user/docs_archive.tar.gz`. The product has recently exited the alpha phase, and the documentation needs to be updated and properly cataloged before being merged into the main repository.

Please complete the following steps:

1. Extract the contents of `/home/user/docs_archive.tar.gz` into a new directory named `/home/user/docs_staging/`.
2. The documentation contains outdated references to the alpha version. Find all Markdown (`.md`) files within `/home/user/docs_staging/` (including all subdirectories) and replace every occurrence of the string `ProductX-v1.0-alpha` with `ProductX-v1.0-stable`.
3. Write a Python script at `/home/user/build_manifest.py` that recursively finds all `.md` files in `/home/user/docs_staging/`, calculates their SHA-256 checksums, and writes the results to `/home/user/manifest.txt`.
4. Run your script to generate `/home/user/manifest.txt`. The format of `manifest.txt` must be strictly:
   `<sha256_hash>  <relative_file_path>`
   - There must be exactly two spaces between the hash and the path.
   - The path must be relative to `/home/user/docs_staging/` (e.g., `api/auth.md`, NOT `./api/auth.md` or `/home/user/docs_staging/api/auth.md`).
   - The lines in the file must be sorted alphabetically by the relative file path.

Ensure the final manifest correctly reflects the updated file contents.