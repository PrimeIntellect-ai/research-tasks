You are acting as an artifact manager curating binary repositories. You have been provided with a nested archive file at `/home/user/repository.tar.gz`.

Your task involves three steps:

1. **Extract all nested archives**: Extract `/home/user/repository.tar.gz` into the directory `/home/user/repository_extracted/`. Then, recursively find and extract any nested archives (`.zip`, `.tar.gz`, `.tar.bz2`) in place (i.e., extract them into the same directory where the archive resides). After successfully extracting an inner archive, delete the inner archive file. Repeat this process until absolutely no archives remain in the directory tree. 

2. **Identify and fingerprint binaries using C++**: Write a C++ program at `/home/user/curator.cpp` that recursively traverses `/home/user/repository_extracted/`. For each file it finds, it must check if the file is an ELF binary. You can determine this by checking if the first 4 bytes of the file match the ELF magic number (`\x7F ELF`, or `7F 45 4C 46` in hex). 

3. **Generate a manifest**: For every ELF binary identified, calculate its SHA-256 checksum. Your C++ program must output a comma-separated values file at `/home/user/manifest.csv`. Each line should be formatted as:
`relative_path,sha256_hex_checksum`
The `relative_path` must be strictly relative to the `/home/user/repository_extracted/` directory (e.g., `moduleA/bin/server`).
The lines in `manifest.csv` must be sorted alphabetically by the `relative_path`.

You may use standard Linux command-line tools for the extraction phase. For the fingerprinting and manifest generation, you MUST use C++. 
Compile your C++ program using:
`g++ -O3 /home/user/curator.cpp -lssl -lcrypto -o /home/user/curator`
Then run it to generate `/home/user/manifest.csv`.