You are an artifact manager tasked with curating a binary repository. We have exported metadata from a legacy artifact storage system into a raw text dump at `/home/user/export.txt`. 

This file contains records of various files, their statuses, and their base64-encoded raw binary payloads.

Each line in the file follows this exact format:
`RECORD ID:<id> | STATUS:<status> | FILE:<filename> | PAYLOAD:<base64_data>`

Your task is to parse this file and generate a standard SHA256 checksum manifest for specific valid binary artifacts. 

Requirements:
1. Filter the records to include ONLY entries where the `STATUS` is exactly `OK` AND the `FILE` name ends with the `.bin` extension.
2. For each matching record, extract the `PAYLOAD` string, decode it from base64 into its original raw binary form, and compute its SHA-256 checksum.
3. Write the results to a manifest file located at `/home/user/valid_bins.manifest`.
4. The manifest file must be formatted exactly like the output of the standard `sha256sum` command: `<sha256_hash>  <filename>` (note the two spaces between the hash and the filename).
5. The entries in the final manifest must be sorted alphabetically by filename.

Ensure your parsing processes the data stream efficiently without loading the entire payload history into memory at once, as the real files can be massive.