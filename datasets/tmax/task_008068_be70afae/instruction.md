You are an artifact manager responsible for curating binary repositories for our internal systems. We have received a batch of compressed artifacts that need to be validated, updated according to our new repository configuration, and moved to a curated directory.

Here is your task:
1. Validate the incoming artifacts located in `/home/user/incoming_artifacts`. You will find several `.tar.gz` archives and a `checksums.sha256` file in this directory. You must verify the SHA-256 checksums of all `.tar.gz` files. Any archive that fails checksum validation should be ignored for curation.
2. Read the curation configuration file at `/home/user/curation_rules.json`. This file maps the base artifact name (the filename without `.tar.gz`) to a list of text replacement rules.
3. For each valid artifact:
   - Extract its contents. Inside, you will find a `metadata.txt` file and a `payload.bin` file.
   - Using Python, apply the transformation rules defined in `/home/user/curation_rules.json` to the `metadata.txt` file. The rules dictate literal search and replace strings (e.g., `{"search": "old_string", "replace": "new_string"}`).
   - Repackage the modified `metadata.txt` and the untouched `payload.bin` into a new archive with the exact same name, saving it to `/home/user/curated_artifacts/` (you will need to create this directory). The archive must be a `.tar.gz` file, and the files (`metadata.txt` and `payload.bin`) must be at the root of the archive (not nested inside a folder).
4. Create a log file at `/home/user/curation_log.txt`. For every archive present in `/home/user/incoming_artifacts`, add a single line to this log. 
   - If the archive passed verification and was curated, write: `SUCCESS: <filename>`
   - If the archive failed checksum verification, write: `FAILED: <filename>`
   Sort the lines in the log file alphabetically.

Ensure your script handles everything end-to-end, as no manual intervention will be allowed once execution begins.