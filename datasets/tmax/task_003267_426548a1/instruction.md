You are an AI assistant helping a technical writer organize a messy export from an old documentation CMS. 

The exported data consists of a multi-line log file and a directory containing raw text and binary asset files. You need to parse the log, extract the files belonging to "PUBLISHED" documents, organize them into a clean directory structure, and generate a cryptographic manifest of the final layout.

Here are the details of your workspace:
- Log file: `/home/user/cms_export.log`
- Raw files directory: `/home/user/raw_assets/` (contains both `.md` text files and `.bin` image/binary files)

The `cms_export.log` file contains multi-line records formatted like this:
```
=== RECORD START ===
DocID: <number>
Title: <Document Title>
TextFile: <filename.md>
AssetFile: <filename.bin>
Status: <PUBLISHED | DRAFT | ARCHIVED>
=== RECORD END ===
```

Your task:
1. Write a Python script to parse `/home/user/cms_export.log`.
2. Find all records where the `Status` is exactly `PUBLISHED`. Ignore all other statuses.
3. For each published record, create a directory inside `/home/user/clean_docs/`. The directory name should be the `Title` converted to lowercase, with all spaces replaced by underscores (e.g., "API Reference" becomes `api_reference`).
4. Copy the corresponding `TextFile` and `AssetFile` from `/home/user/raw_assets/` into this new directory.
5. After all files are organized, generate a SHA-256 checksum manifest of every file inside `/home/user/clean_docs/` (excluding the manifest itself). Save this manifest to `/home/user/clean_docs/manifest.sha256`.

Manifest format requirements:
- The manifest must contain one line per file.
- Format: `<sha256_hash>  <relative_path_from_clean_docs>` (note the two spaces between hash and path, standard for `sha256sum`).
- For example: `a1b2...c3d4  api_reference/doc1.md`
- The lines in the manifest must be sorted alphabetically by the relative file path.

Do not use absolute paths in the manifest. All file paths in the manifest must be relative to `/home/user/clean_docs/`.