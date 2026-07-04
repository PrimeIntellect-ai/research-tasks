We are porting a legacy web-security tool into a minimal container environment. As part of this effort, we need to replace an old, stripped binary payload sanitizer (`/app/legacy_sanitizer`) with a newly written version from source, because the legacy version cannot be rebuilt for our new architecture.

We have a draft C implementation at `/home/user/sanitizer_draft.c`. It attempts to emulate the exact behavior of the legacy binary: it takes a string via standard input, performs URL decoding (converting `%XX` to the corresponding ASCII character), strips any occurrence of the exact substring `<script>`, and prints the result to standard output. 

However, the draft C implementation has two problems:
1. It contains a memory safety vulnerability (Undefined Behavior / Buffer Overflow) when a `%` character appears at the very end of the input or is followed by invalid hex characters.
2. It fails to perfectly match the output of `/app/legacy_sanitizer` due to these parsing bugs.

Your tasks:
1. Debug and fix the C/C++ memory safety issues in `/home/user/sanitizer_draft.c` so that it safely handles all malformed inputs.
2. Compile your fixed version to `/home/user/sanitizer_fixed` (using `gcc -O2`). Your fixed binary must be strictly bit-exact equivalent in its I/O behavior to the oracle binary at `/app/legacy_sanitizer` for all possible inputs.
3. To ensure we don't regress, set up a minimal CI/CD test script in Bash at `/home/user/ci_test.sh`. This script must:
   - Accept no arguments.
   - Run `/home/user/sanitizer_fixed` against at least three hardcoded test payloads (including at least one malicious `<script>` payload and one malformed `%` payload).
   - Compare the output against the expected safe output.
   - Exit with status code `0` if all tests pass, and `1` if any fail.
   - Be marked as executable.

Ensure your compiled binary `/home/user/sanitizer_fixed` is ready for rigorous fuzz testing against the legacy oracle.