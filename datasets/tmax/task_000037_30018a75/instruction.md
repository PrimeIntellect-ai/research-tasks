You are assisting a technical writer who is organizing and updating a batch of legacy documentation files for a new product release. 

The raw documentation files are located in `/home/user/docs_raw/`. All files are in Markdown format (`.md`). 

You need to write a Python script at `/home/user/pack_docs.py` and run it to perform the following operations:

1. **Text Transformation**: Read all `.md` files in `/home/user/docs_raw/`. In the text of each file, globally replace the deprecated company name `AcmeCorp` with `ZenithInc`, and update the version string `v1.0` to `v2.0`.
2. **Manifest Generation**: Calculate the SHA256 checksum (hexadecimal) of the *transformed* content for each file.
3. **Custom Compression**: Create a custom archive format. The archive should be a single zlib-compressed JSON object. The uncompressed JSON must have exactly this structure:
   ```json
   {
     "manifest": {
       "intro.md": "<sha256_of_transformed_intro>",
       "setup.md": "<sha256_of_transformed_setup>",
       ...
     },
     "files": {
       "intro.md": "<transformed_content_of_intro>",
       "setup.md": "<transformed_content_of_setup>",
       ...
     }
   }
   ```
4. **Atomic Write**: The documentation compiler relies on file system watchers, so the final archive must be written atomically. Your script must first write the compressed data to a temporary file (e.g., `/home/user/release.tmp`) and then atomically rename it to `/home/user/release.docpack`.

Run your script to generate `/home/user/release.docpack`. 

Constraints:
- Use Python 3.
- Only use standard library modules (e.g., `os`, `json`, `zlib`, `hashlib`, `tempfile`).
- Do not leave any temporary files behind.