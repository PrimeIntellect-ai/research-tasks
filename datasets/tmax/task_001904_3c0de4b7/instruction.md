You are a developer organizing a set of project files stored in a custom archive format. 

In `/home/user/project`, you will find a custom packed archive named `archive.pack`. The format of this file is as follows:
1. A JSON header detailing the files contained within. Example: `{"files":[{"name":"config.json","offset":0,"size":22},{"name":"firmware.elf","offset":22,"size":16}]}`
2. A single null byte (`\0`) acting as a separator.
3. The contiguous binary payload containing the raw data for each file, where `offset` is relative to the start of this binary payload section (immediately after the null byte).

Your task is to:
1. Write a C++ program named `/home/user/project/extractor.cpp` that parses `archive.pack` and extracts the files into a new directory: `/home/user/project/extracted/`. 
   - A single-header JSON library is provided at `/home/user/project/json.hpp` for you to use in your C++ code. Include it via `#include "json.hpp"`.
2. Compile and run your C++ extractor.
3. Using standard bash commands, generate a manifest file at `/home/user/project/manifest.csv` that contains the SHA256 checksums of the extracted files. The format must be strictly `filename,sha256hash` (e.g., `config.json,d2a...` with no paths in the filename column, and no extra spaces).
4. Create a compressed tarball named `/home/user/project/release.tar.gz` containing the `manifest.csv` file and the `extracted/` directory.

Ensure all paths in your commands and scripts are absolute where necessary, or execute them from within the `/home/user/project` directory.