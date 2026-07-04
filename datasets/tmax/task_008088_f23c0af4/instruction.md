You are a build engineer responsible for an automated artifact verification pipeline. 

Recently, the custom C-based artifact verification tool (`/home/user/src/verifier.c`) has started crashing with segmentation faults and double-free errors when processing certain artifact files. Your pipeline needs this tool to generate checksums and error-correcting parity blocks for build artifacts before they are packaged.

Your tasks are to:
1. Debug and repair `/home/user/src/verifier.c` so that it is memory safe, contains no undefined behavior, and correctly processes all files without crashing.
2. Compile the fixed `verifier.c` into an executable at `/home/user/bin/verifier`.
3. Use your preferred scripting language (e.g., Python, Node.js, or Bash) to write a packaging script at `/home/user/package_artifacts.sh` (or `.py`/`.js`). This script must:
   - Create a virtual environment or local package configuration if using Python/Node.
   - Run `/home/user/bin/verifier` on all `.bin` files located in `/home/user/artifacts/`.
   - Collect the stdout from the verifier.
   - Write a final JSON report to `/home/user/verified_checksums.json` where the keys are the base filenames (e.g., `app_v1.bin`) and the values are the exact hexadecimal string output by the verifier.

The buggy C file `/home/user/src/verifier.c` contains custom checksum logic. You must NOT alter the core mathematical logic of the checksum (the bitwise operations inside the loop), but you MUST fix the loop boundaries, memory allocations, and memory deallocations to prevent crashes and out-of-bounds reads.

Ensure that `/home/user/verified_checksums.json` is perfectly formatted JSON.