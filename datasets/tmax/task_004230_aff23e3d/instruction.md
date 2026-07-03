You are a build engineer responsible for artifact management and serialization processing. We have a custom artifact parsing pipeline that currently has a few broken components.

There is a vendored Python package located at `/app/vendored/artifact_parser-1.2.0`. This package uses a C extension to quickly deserialize binary artifact manifests. However, the package has a known memory safety bug (an out-of-bounds read) in `src/parser.c` that causes it to segfault on malformed inputs. 

Additionally, there is a Go-based artifact fetching tool at `/app/build_tool` that is failing to build due to a circular import between its `cmd` and `core` packages.

Your objectives:
1. Navigate to `/app/build_tool`, fix the Go circular import, and compile the tool. Use it to generate test fixtures (it outputs to `/tmp/fixtures`).
2. Fix the memory safety issue in the C extension of the `artifact_parser` package in `/app/vendored/artifact_parser-1.2.0/src/parser.c`. Specifically, it reads a length field but fails to verify that the remaining buffer is large enough before calling `memcpy`. 
3. Build and install the fixed `artifact_parser` Python package.
4. Write a Python script at `/home/user/process_artifacts.py` that takes a single file path as a command-line argument. The script must read the file, use `artifact_parser.parse_manifest(data)` (which returns a list of artifact names), sort the list of names alphabetically, and print the resulting list as a JSON array to standard output. If `parse_manifest` raises a `ValueError` or returns `None` (for malformed data), print `["ERROR"]`.

Your Python script will be rigorously tested against an internal reference implementation using fuzz testing. It must produce exactly the same JSON output for any arbitrary binary input file without crashing.