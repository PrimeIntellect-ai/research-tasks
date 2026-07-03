I am a technical writer responsible for organizing a massive repository of legacy documentation. Our documentation is stored in nested, multi-part custom archives. To extract and organize these safely, we use a custom C utility called `doctar` which verifies archive integrity and sanitizes internal virtual filesystem paths before mounting or extracting them.

However, the source code we were handed for this utility is slightly broken. It is located in `/app/doctar-1.0`. 

There are two major issues I need you to fix:
1. The `Makefile` has a configuration error preventing it from compiling.
2. The path sanitization logic in `sanitize.c` (specifically the `normalize_doc_path` function) is buggy. It is supposed to take an internal archive path string and resolve all `.` and `..` components, as well as remove duplicate slashes `//`, returning a canonicalized path. For example, `docs/v1//../v2/./api.md` should become `docs/v2/api.md`. Currently, it fails on complex relative traversals.

I have a pre-compiled, correct reference binary (without the source) that our CI system uses, located at `/opt/oracle/doctar_oracle`. 

Your task is to:
1. Fix the `Makefile` so that running `make` successfully builds the `doctar_sanitize` executable.
2. Rewrite or fix the `normalize_doc_path` function in `sanitize.c` so that its behavior is exactly bit-for-bit identical to the oracle binary for any given path input.

The executable takes a single argument (the path to sanitize) and prints the sanitized path to standard output.
Example usage:
`/app/doctar-1.0/doctar_sanitize "a/b/../c"`

Our automated verification system will extensively test your compiled binary against the oracle with thousands of random path strings to ensure the outputs match exactly. Please leave the compiled, working `doctar_sanitize` binary at `/app/doctar-1.0/doctar_sanitize`.