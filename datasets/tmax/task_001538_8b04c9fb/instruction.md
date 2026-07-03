I am a technical writer and I regularly receive documentation dumps from various engineering teams. They often send these as multi-part archives, and sometimes they nest zip files inside those archives. It's a mess. 

I need you to write a Bash script for me that automates the extraction and indexing of these files. 

Please create a script at `/home/user/process_docs.sh`. The script should do the following:

1. **Concurrency Control:** Because this script might be triggered multiple times simultaneously by a cron job, it must use `flock` to ensure only one instance of the extraction logic runs at a time. Use `/tmp/docs_process.lock` as the lock file.
2. **Reassembly and Extraction:** 
   - Look in the `/home/user/docs_drop/` directory for a multi-part archive named `docs_archive.tar.gz.part*`.
   - Reassemble these parts into a single gzip-compressed tarball.
   - Extract the contents into `/home/user/docs_extracted/`.
3. **Nested Archives:** 
   - After the initial extraction, recursively search through `/home/user/docs_extracted/` for any nested `.zip` archives.
   - Extract any found `.zip` archives into the same directory where the zip file is located.
   - Remove the nested `.zip` files after extraction to save space.
4. **Manifest Generation:** 
   - Find all Markdown (`.md`) files within `/home/user/docs_extracted/` (including those extracted from nested archives).
   - Generate a checksum manifest file at `/home/user/docs_manifest.txt`.
   - The manifest must contain the SHA256 checksum of each `.md` file.
   - The format must be exactly what `sha256sum` outputs, but using *relative paths* starting from the `/home/user/docs_extracted/` directory (e.g., `e3b0c4...  api/v1/endpoints.md`).
   - The entries in the manifest must be sorted alphabetically by the file path.

Make sure your script is executable. You can assume the multi-part archive is already placed in `/home/user/docs_drop/`.