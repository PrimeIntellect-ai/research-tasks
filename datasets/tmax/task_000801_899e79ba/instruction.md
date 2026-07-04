You are a platform engineer maintaining a CI/CD pipeline. A recent CMake build job failed during the linking phase because it couldn't locate several shared libraries. 

The build artifact directory at `/home/user/ci_artifacts/` contains two files:
1. `/home/user/ci_artifacts/link_error.log`: The raw standard error output from the linker.
2. `/home/user/ci_artifacts/registry.dat`: A custom-encoded artifact registry containing paths to pre-built libraries in the CI cache.

The artifact registry (`registry.dat`) uses a strict custom encoding format to prevent corruption during transport. Each line is formatted as:
`[HEX_ENCODED_LIBNAME]:[BASE64_ENCODED_PATH]:[MD5_CHECKSUM]`

- `HEX_ENCODED_LIBNAME`: The library name (e.g., `foo` for `-lfoo`) encoded in plain hexadecimal.
- `BASE64_ENCODED_PATH`: The absolute file path to the library, encoded in Base64.
- `MD5_CHECKSUM`: The MD5 hash of the *decoded, plain-text path string* (exactly as decoded, with no trailing newlines added before hashing).

Your task is to:
1. Construct a script or use shell commands to parse `/home/user/ci_artifacts/link_error.log` to identify all missing libraries. Missing libraries are indicated by lines containing exactly the pattern: `cannot find -l<libname>` (e.g., `cannot find -lmathutils`).
2. For each missing library identified in the log, look up its entry in `/home/user/ci_artifacts/registry.dat`.
3. Decode the path and **verify its integrity** by computing the MD5 sum of the decoded path string. If the computed MD5 does not match the MD5 in the registry, ignore that entry (it is corrupted).
4. Output the verified, decoded absolute paths of the missing libraries to a new file at `/home/user/ci_artifacts/recovered_paths.txt`.
5. The output file must contain exactly one path per line, and the lines must be sorted alphabetically.

Write the necessary code/commands to accomplish this. You can use any programming language or standard command-line tools available in the environment.