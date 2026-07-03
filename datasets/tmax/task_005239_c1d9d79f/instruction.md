You are an AI assistant helping a data researcher organize and sanitize a massive collection of scientific datasets. The researcher has been collecting datasets from various sensors. Due to a concurrent log rotation script racing with the writing process, several dataset archives are corrupted, truncated, or contain unsafe path traversal structures.

Your goal is to build a C-based filter utility to sanitize these dataset archives. 

We have provided a vendored archive processing library at `/app/libtar-1.2.20` that you must use to inspect the archives. However, the researcher mentioned that the build system for this library has a slight issue on modern Linux environments and currently fails to compile.

Here is what you need to do:

1. **Fix and Compile the Vendored Library**: 
   Navigate to `/app/libtar-1.2.20`. Identify and fix the compilation issue (hint: it's related to missing macros for `makedev` in `lib/compat.c` or similar system headers depending on the environment). Build and install it locally in a directory of your choice (e.g., `/home/user/local`).

2. **Configuration File Interpretation**:
   Create a C program at `/home/user/dataset_filter.c`. This program must first read a configuration file located at `/home/user/filter.conf`. The config file contains two lines:
   `ALLOWED_PREFIX=dataset_`
   `MAX_FILES=100`

3. **Archive Integrity and Security Verification**:
   Your C program must read a TAR archive passed via **standard input (stdin)**. 
   It should use the fixed `libtar` library to iterate through the archive headers.
   The program must REJECT the archive (exit code 1) if:
   - The archive is truncated or corrupted (fails integrity).
   - Any file in the archive uses absolute paths (e.g., starts with `/`).
   - Any file in the archive attempts path traversal (contains `../`).
   - The number of files exceeds `MAX_FILES` (from the config).
   - Any file in the archive does NOT start with `ALLOWED_PREFIX` (from the config) in its base name.

   If the archive is perfectly valid and safe, the program should ACCEPT it (exit code 0).

4. **Integration**:
   Compile your `dataset_filter.c` into an executable named `/home/user/dataset_filter`, linking against your locally built `libtar`.

Your final executable will be tested automatically by piping various archives into it. Ensure it relies strictly on standard input and returns the correct exit codes.