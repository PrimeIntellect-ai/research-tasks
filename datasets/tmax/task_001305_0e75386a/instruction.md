You are a technical writer tasked with organizing a large archive of legacy documentation. 

The documentation is stored in a custom binary format archive at `/home/user/legacy_docs.dat`. Each record in the archive consists of a binary header followed by a JSON metadata payload and compressed Markdown text. 

Your organization previously developed a Python tool to extract the metadata from these archives, located at `/app/legacy-doc-parser-1.2.0`. However, the tool is currently broken. It fails to parse the binary headers correctly and crashes when run against the archive.

Your objectives:
1. Identify and fix the deliberate bug in the vendored `legacy-doc-parser` package so that it successfully parses the binary file.
2. Use the fixed tool to extract the JSON metadata stream from `/home/user/legacy_docs.dat`.
3. Process the extracted JSON metadata to create a concise index of the documentation. Using standard shell tools (like `jq`, `awk`, or `sed`), extract ONLY the `doc_id` and `category` fields for every record.
4. Format the extracted fields as a CSV (with no header row, just `doc_id,category`) and compress it into a gzip file at `/home/user/summary.csv.gz`.

To pass the automated verification, your final compressed index must be extremely lean. The test suite will measure the file size of `/home/user/summary.csv.gz`, and it must be strictly **less than 250 bytes**.

Ensure your final output file is exactly at `/home/user/summary.csv.gz`.