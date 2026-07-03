I am a technical writer and I need help organizing and transforming a batch of legacy documentation drafts. The files are currently located in `/home/user/raw_docs/` and are named in the format `draft_NNN_topic.txt` (e.g., `draft_001_intro.txt`). 

Please perform the following pipeline to transform, rename, verify, and compress these files:

1. **Text Transformation (Piping & Python)**: 
   Write a Python script at `/home/user/transformer.py` that reads text from `stdin` and writes to `stdout`. 
   The input text will always start with three lines of metadata in this format:
   `Title: <text>`
   `Author: <text>`
   `Date: <text>`
   
   Your script must transform these first three lines into standard YAML frontmatter:
   ```yaml
   ---
   title: <text>
   author: <text>
   date: <text>
   ---
   ```
   Leave the rest of the text content exactly as is, including any empty lines following the metadata.

2. **Bulk Processing and Renaming**:
   Create a new directory `/home/user/processed_docs/`. 
   For every `.txt` file in `raw_docs`, pipe its contents through your `transformer.py` script and save the output in `processed_docs`.
   While saving, rename the files to swap the `NNN` and `topic` parts and change the extension to `.md`. For example, `draft_001_intro.txt` must become `intro_001.md`.

3. **Manifest Generation**:
   Generate a SHA256 checksum manifest of all the newly created `.md` files. Save this manifest to `/home/user/processed_docs/manifest.txt`. The manifest should contain only the base filenames (e.g., `intro_001.md`), not their absolute paths, following standard `sha256sum` format.

4. **Custom Compression**:
   Write a Python script `/home/user/compress.py` that reads all `.md` files in `/home/user/processed_docs/`, compresses their raw contents using Python's standard `zlib` library, and writes the compressed bytes to new files with the extension `.md.zlib`. 
   After generating the `.zlib` files, delete the uncompressed `.md` files. (Do not compress or delete `manifest.txt`).

When you are finished, `/home/user/processed_docs/` should contain exactly the `manifest.txt` file and the `.md.zlib` files.