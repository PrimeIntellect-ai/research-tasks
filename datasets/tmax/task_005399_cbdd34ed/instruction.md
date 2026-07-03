You are a technical writer managing a documentation pipeline. Contributors submit documentation as `.tar` archives. Unfortunately, some archives are maliciously crafted to contain "tar slip" vulnerabilities (directory traversal paths that overwrite files outside the extraction directory). 

Your task is to build a C-based processing tool that safely handles these archives, transforms outdated terms in the documents, and produces a summary report.

Write a C program at `/home/user/process_docs.c` and compile it to `/home/user/process_docs`. When run, it must perform the following steps:

1. **Scan**: Look for all `.tar` files in `/home/user/docs_incoming/`.
2. **Integrity Verification**: Check each `.tar` archive for tar slip vulnerabilities. An archive is considered malicious if ANY of its internal file paths contain the substring `../` or start with `/`. You may read the tar headers directly in C or use shell commands like `tar -tf` via `popen`.
3. **Quarantine**: If an archive is malicious, move the original `.tar` file to `/home/user/quarantine/` and do not extract it.
4. **Extraction**: If an archive is safe, create a directory at `/home/user/extracted_docs/<archive_name_without_extension>/` (e.g., `/home/user/extracted_docs/docA/`) and extract the archive's contents into that directory.
5. **Structured Parsing & Transformation**: Inside each extracted directory, there is a `toc.csv` file with a header (e.g., `file,status`). Parse this CSV. For every file listed under the `file` column, perform a text transformation: replace all occurrences of the exact string `DRAFT` with `FINAL`. You can implement this text replacement in pure C or invoke tools like `sed` via `system()`.
6. **Reporting**: Create a JSON log file at `/home/user/processing_summary.json` containing the alphabetical lists of processed and quarantined tar files. The format must exactly match:
```json
{
  "processed": [
    "docA.tar",
    "docC.tar"
  ],
  "quarantined": [
    "docB.tar"
  ]
}
```

Ensure your C program completes all these steps successfully when executed without arguments. Leave the compiled executable at `/home/user/process_docs` and run it once so the final system state reflects the processed documents.