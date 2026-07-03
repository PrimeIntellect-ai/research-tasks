You are a Build Engineer at a software company. We have a legacy artifact packaging pipeline that is currently bottlenecked by a slow, proprietary packaging tool located at `/app/legacy_packer`. 

This tool takes a directory of build artifacts, filters them based on a minimum Semantic Version, and packs the qualifying artifacts into a custom binary archive format with integrity checksums. Unfortunately, the source code was lost, and the executable is a stripped binary. 

Your task is to write a highly optimized replacement in C, named `fast_packer`, which produces byte-for-byte identical output archives but runs significantly faster.

Requirements:
1. **Reverse Engineer the Format**: Run `/app/legacy_packer` on some dummy files to deduce the custom archive format. 
   - Usage: `/app/legacy_packer <input_dir> <min_semver> <output_file>`
   - `input_dir` contains dummy artifact files named in the format `artifact_<major>.<minor>.<patch>.bin` (e.g., `artifact_1.2.3.bin`).
   - `min_semver` is a strict lower bound (e.g., `1.2.0`). Only files with a semantic version *strictly greater* than `min_semver` should be included in the archive. 
   - Files packed in the archive must be ordered lexicographically by their filename.

2. **Implement in C**: 
   - Create your implementation in `/home/user/src/fast_packer.c`.
   - Your implementation must correctly parse standard Semantic Versions (Major.Minor.Patch) and apply the strict greater-than logic.
   - It must compute whatever custom data structure/integrity code the legacy tool uses per file.

3. **Polyglot Build Orchestration**:
   - Write a `Makefile` in `/home/user/src/` that compiles `fast_packer.c` into a binary named `fast_packer` using `gcc` with maximum optimizations (e.g., `-O3`).
   - The Makefile should have an `all` target that builds the binary.

4. **Performance Target**:
   - Your C implementation must be aggressively optimized. It will be tested against a massive directory of 50,000 artifacts. 
   - It must achieve a runtime speedup of at least 3.0x compared to `/app/legacy_packer` on the same dataset, while producing the exact same output file checksum.

Once you have created and built `fast_packer`, test it against `/app/legacy_packer` to ensure the output files are identical. Create a log file at `/home/user/verification.log` containing the MD5 hashes of the outputs from both tools on a test directory of your choosing to prove they match.