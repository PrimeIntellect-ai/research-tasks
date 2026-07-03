I am a technical writer trying to organize a large batch of raw documentation files, but the system generating them is messy. I have a directory at `/home/user/docs_raw` containing many `.txt` files. Some are drafts, and some are final. 

I need you to write and execute a Bash script at `/home/user/process_docs.sh` that does the following:

1. **Metadata-based search:** Find all `.txt` files in `/home/user/docs_raw` that contain the exact string `STATUS: FINAL`. Ignore any files that do not contain this string.
2. **Format conversion & Text editing:** For each "FINAL" file:
   - Convert the formatting by replacing any line starting with `[HEADER] ` (including the space) with `# ` (e.g., `[HEADER] System Setup` becomes `# System Setup`).
   - Save the converted content as a Markdown file (`.md`) using the same base filename in a temporary directory.
3. **Custom compression:** 
   - Bundle all the newly formatted `.md` files into a single `tar` archive.
   - Compress the `tar` archive using `gzip`.
   - Create a custom archive format file at `/home/user/final_docs.cgz`. This file must start with exactly the string `DOCARCHIVE_V1` followed by a single newline character (`\n`), immediately followed by the raw binary data of the gzipped tarball.

Your script must handle the creation of the final `/home/user/final_docs.cgz` file. Please write the script, ensure it is executable, and run it so the final archive is generated. 

Note: Do not delete the original files in `/home/user/docs_raw`.