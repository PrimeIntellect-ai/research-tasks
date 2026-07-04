You are a mobile build engineer tasked with fixing a broken dependency resolution pipeline. The pipeline merges dependency manifests from different mobile teams, choosing the highest semantic version for each library, and relies on a fast C++ native extension to parse the version strings. 

Recently, the pipeline started crashing with a segmentation fault when processing unusually long pre-release version strings, and it's also making incorrect version comparisons (e.g., it thinks "1.2.3" is newer than "1.2.10").

Your workspace is located at `/home/user/mobile_pipeline/`.

Here are your objectives:
1. **Fix the C++ Memory Safety Issue**: The native library `fast_semver.cpp` has a memory safety bug (buffer overflow) in the `parse_version_core` function. Fix this file so it safely handles long version strings.
2. **Build the Native Extension**: Use the provided `Makefile` to compile the native library (`make all`). It builds `libfastsemver.so`.
3. **Fix Semantic Version Comparison in Python**: The script `build_resolver.py` uses naive string comparison for versions, which fails for numbers > 9. Update the `compare_versions(v1, v2)` function in `build_resolver.py` to properly parse and compare semantic versions (e.g., "1.2.10" > "1.2.3"). You may assume versions only contain integers separated by dots (e.g., "X.Y.Z"), and optionally a hyphen for pre-release (which the C++ library handles by extracting the base version).
4. **Merge and Sort**: Run `python3 build_resolver.py manifest_A.json manifest_B.json`. The script should output a file exactly at `/home/user/mobile_pipeline/resolved_manifest.json`. The output must be a well-formatted JSON dictionary (indent=4) where keys are sorted alphabetically, containing the highest version of each dependency found in either A or B.

Do not use external Python libraries like `semver`; implement the standard numeric version comparison manually in the script. Ensure all files are in their correct final state and the output JSON exactly matches the expected resolution.