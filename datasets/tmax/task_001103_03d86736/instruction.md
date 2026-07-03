You are an artifact manager for a binary repository.
We have a Python package pre-vendored at `/app/vendored/artifact_curator-1.2.0`. It is designed to extract artifact archives (tar files), parse their bundled XML metadata, convert the metadata to JSON, and create hard links to deduplicate identical binaries.

However, the package currently has two significant flaws:
1. A critical "tar slip" vulnerability in `artifact_curator/extractor.py`. Malicious archives can write files outside the intended extraction directory if the archive members contain path traversals (like `../` or absolute paths).
2. A severe performance bottleneck in the deduplication logic in `artifact_curator/dedup.py`. It currently compares every newly extracted binary to every previously extracted binary byte-by-byte (O(N^2)).

Your task:
1. Fix the `artifact_curator` package in `/app/vendored/artifact_curator-1.2.0` to safely skip any archive members that attempt to traverse outside the target directory.
2. Optimize the deduplication logic in `artifact_curator/dedup.py` to use cryptographic hashing (e.g., SHA256) so it runs in O(N) time.
3. Install the fixed package locally so the `artifact-curator` CLI is available.
4. Write a bash script `/home/user/process_all.sh` that uses the `artifact-curator` CLI to process all `.tar` archives in `/home/user/incoming/` and outputs the extracted and deduplicated artifacts to `/home/user/processed/`. 

Performance Requirement:
The automated test will measure the execution time of your `/home/user/process_all.sh` script on a dataset of 100 archives. The total execution time must be less than 2.0 seconds (the unoptimized version takes over 20 seconds). 

Security Constraint:
No files must be written outside `/home/user/processed/` during the extraction. Any archive trying to write to directories like `/home/user/system_fake/` must have those specific malicious files skipped without aborting the rest of the archive extraction.

Make sure your `/home/user/process_all.sh` script is executable.