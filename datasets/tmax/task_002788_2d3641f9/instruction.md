You are assisting a technical writer in organizing and updating a documentation repository. 

The documentation is stored in the directory `/home/user/docs`. It contains various files, including Markdown documents (`.md`). Some files are drafts, while others are published. Published files can be identified by the exact string `status: published` appearing somewhere in the file (typically in the frontmatter).

Your task is to perform the following operations:
1. Search through `/home/user/docs` to find all Markdown (`.md`) files that are marked as published.
2. In those published Markdown files *only*, replace every occurrence of the string `LegacyBrand` with `NovaBrand`.
3. To prevent partial writes in case of an interruption, you must perform these updates atomically. Do this by writing a short script (in bash, python, or your language of choice) that reads the original file, performs the text replacement, writes the output to a temporary file in the same directory, and then renames the temporary file to overwrite the original file. 
4. Generate a SHA-256 checksum manifest of *only* the published Markdown files that you processed. Save this manifest to `/home/user/docs/manifest.sha256`. The file should be in the standard format produced by the `sha256sum` command (e.g., `<hash>  <filename>`).

Do not modify any files that are not Markdown files, and do not modify any Markdown files that do not contain `status: published`.