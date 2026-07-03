You are a build engineer responsible for securing our local artifact mirror. Recently, our build system failed to link a critical shared library because the artifact mirror was partially corrupted—some files were tampered with, and others have incorrect checksums. 

Your task is to write a secure dependency resolver in Python that finds the correct, uncorrupted shared library for a given version constraint.

The artifact mirror is located at `/home/user/mirror/`. Inside, there is an index file at `/home/user/mirror/index.csv` with the following format:
`DependencyName,Version,Base64EncodedFilename,ExpectedSHA256`

Write a Python script at `/home/user/resolve.py` that does the following:
1. Accepts a dependency constraint string as a command-line argument (e.g., `"libcore >= 1.2.0, < 2.0.0"`). The operators to support are `>=`, `<=`, `>`, `<`, and `==`. Multiple constraints will be separated by a comma and a space.
2. Reads and parses `/home/user/mirror/index.csv`.
3. Filters the index for the specified `DependencyName` that satisfies ALL the given semantic version constraints. (You must implement semantic version comparison; do not assume simple string sorting works for versions like `1.10.0` vs `1.2.0`).
4. Decodes the `Base64EncodedFilename` to get the actual filename of the shared library.
5. Verifies the SHA256 checksum of the actual file in `/home/user/mirror/<decoded_filename>`. If the computed SHA256 hash does not exactly match the `ExpectedSHA256` in the index, the file is corrupted and must be ignored.
6. Among the valid, uncorrupted files that meet the version constraints, selects the one with the HIGHEST semantic version.
7. Writes the absolute path of this selected file to `/home/user/link_target.txt`.

Once you have written the script, execute it with the following constraint:
`python3 /home/user/resolve.py "libcore >= 1.2.0, < 2.0.0"`

Ensure that `/home/user/link_target.txt` contains exactly the absolute path to the correct `.so` file, with no extra whitespace or newlines.