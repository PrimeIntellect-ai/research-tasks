We are migrating our legacy package management backend and running into a C library linking issue. We use a vendored C library for semantic versioning, located at `/app/libsemver-v1.0.0/`. However, our build system requires it to be compiled as a shared library (`libsemver.so`), but the provided `Makefile` is broken—the `shared` target fails to build because the object files aren't compiled with the correct position-independent code flags.

Your tasks:
1. Debug and fix the `Makefile` in `/app/libsemver-v1.0.0/` so that running `make shared` successfully produces `libsemver.so`.
2. We have a legacy Perl script at `/app/legacy_check.pl` that attempts to filter valid and invalid semantic versions using regular expressions. It is buggy and vulnerable to malicious inputs. Translate its high-level intent into a new program (written in any language you choose, e.g., Python using `ctypes`, C, etc.) that explicitly links against the fixed `libsemver.so` to parse versions.
3. Your new program must act as a strict sanitiser. Create an executable script or binary at `/home/user/version_filter`. It must accept two arguments: an input file path and an output file path.
   Usage: `/home/user/version_filter <input_file> <output_file>`
   It should read the input file line-by-line, and write ONLY the syntactically valid semantic versions to the output file (one per line). A version is valid if and only if `libsemver.so` can successfully parse it without error or crashing.
4. Your filter must be robust against adversarial inputs (e.g., extremely long strings, malformed fields) which might cause segmentation faults in poorly written wrappers. 

Ensure your `/home/user/version_filter` is executable and outputs exactly the preserved valid strings in the same order.