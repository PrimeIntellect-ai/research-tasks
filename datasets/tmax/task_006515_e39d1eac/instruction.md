You are an artifact manager tasked with curating a raw dump of binary repositories. You have received a batch of uploaded files, a vendor manifest in JSON, and a multi-line ingestion log. However, some of the archives were corrupted during transit, and others suffered bit-rot (their current SHA-256 checksums do not match the expected ones logged during ingestion).

Your task is to write a Bash script at `/home/user/curate.sh` that performs the following steps:

1.  **Parse Inputs**: Read the vendor manifest at `/home/user/raw_drop/vendor_manifest.json`. It contains a JSON array of objects with `file`, `project`, and `arch` keys.
2.  **Extract Checksums**: Parse the multi-line log file at `/home/user/raw_drop/ingest.log`. Each record is bounded by `[START]` and `[END]` and contains fields like `File: <filename>` and `SHA256: <expected_hash>`. Extract the expected SHA256 checksum for each file.
3.  **Verify Integrity**: For each file listed in the manifest (located in `/home/user/raw_drop/`):
    *   Test the archive integrity. If it's a `.tar.gz`, use `tar -tzf`. If it's a `.zip`, use `unzip -t`. Exclude any file that fails this integrity check.
    *   Compute its current SHA256 checksum and compare it against the expected hash from `ingest.log`. Exclude any file that has a checksum mismatch.
4.  **Reorganize**: For the valid files passing both checks, move them to a new directory structure: `/home/user/curated/<arch>/<project>/<file>`.
5.  **Generate New Manifest**: Create a CSV file at `/home/user/curated/verified_manifest.csv` with the header `filename,architecture,project,sha256`. Add a row for each valid, reorganized file containing its details and actual checksum. Sort the rows (excluding the header) alphabetically by filename.

You must execute your script to ensure the `/home/user/curated` directory is populated correctly. Use `jq` and standard Bash utilities.