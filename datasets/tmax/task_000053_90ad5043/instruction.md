You are an infrastructure engineer organizing cross-compiled release artifacts for a distributed system. The CI/CD pipeline has dumped all recent builds into a single directory, but some files were corrupted during transfer. 

Your task is to write a Python script `/home/user/organizer.py` that validates, filters, and organizes these artifacts based on their checksums and Semantic Versioning (SemVer).

Here is the current state of the system:
- A directory `/home/user/artifacts/` contains several binary files named using the pattern: `worker_v<semver>_<os>_<arch>.bin` (e.g., `worker_v1.2.3_linux_amd64.bin`).
- Inside the same directory, there is a file named `checksums.txt` containing SHA256 hashes for all the files, in the standard `sha256sum` output format (`<hash>  <filename>`).

Your script `/home/user/organizer.py` must perform the following actions:
1. **Mathematical Validation**: Read `checksums.txt` and compute the actual SHA256 checksum for each binary. Discard any files whose computed hash does not perfectly match the hash listed in `checksums.txt`.
2. **SemVer Organization**: For the mathematically valid files, parse the `<semver>` from the filename. Move the file to a new directory structure under `/home/user/organized/` following this pattern:
   `/home/user/organized/<major>.<minor>/<os>/<arch>/<filename>`
   (e.g., `/home/user/organized/1.2/linux/amd64/worker_v1.2.3_linux_amd64.bin`).
3. **Version Comparison**: Determine the absolute highest *stable* semantic version among the valid files. A stable version is one that does NOT contain a pre-release identifier (like `-alpha`, `-beta`, etc.).
4. **Mock Setup**: In the directory where the highest stable version's binary is placed, create a test fixture file named `mock_env.json` containing exactly: `{"test_mode": true, "version": "<highest_stable_version>"}`.
5. Write the highest stable version string (e.g., `2.0.1`) to a file at `/home/user/latest_version.txt`.

Run your script to process the artifacts. You may use standard library modules or `packaging.version` if available.