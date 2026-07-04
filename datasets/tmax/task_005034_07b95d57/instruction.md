You are acting as a Build Engineer managing an artifact pipeline. We are in the middle of modernizing our build system and artifact manifests. You need to fix a broken C/C++ build, translate a legacy script, and perform a schema migration on our artifact manifest.

Here is the current state of the system in `/home/user/workspace`:

1. **The Build System (CMake & Shared Libraries)**
   In `/home/user/workspace/builder`, there is a CMake project that compiles a shared library (`libarchiver.so`) and an executable (`packager`). The executable uses a checksum routine from the shared library.
   Currently, the build fails at the link stage, or the resulting executable fails to run because it cannot find the shared library. 
   - Fix the `CMakeLists.txt` so that the `packager` target properly links against the `archiver` shared library.
   - Ensure that the compiled `packager` binary can be executed directly from the build directory (e.g., using RPATH) without requiring `LD_LIBRARY_PATH` to be set manually.
   - Build the project in `/home/user/workspace/builder/build`.

2. **Code Translation & Checksums**
   We have a legacy Ruby script at `/home/user/workspace/legacy_manifest.rb`. It reads a v1 artifact manifest (`artifacts.json`), migrates the schema to v2, and prints the result. 
   - Translate this Ruby script into a Python 3 script named `/home/user/workspace/manifest.py`.
   - The Ruby script currently hardcodes the checksum as `"PENDING"`. Your Python script must instead execute the built `packager` binary (located at `/home/user/workspace/builder/build/packager`) on each artifact file path to compute the actual hex checksum.

3. **Schema Migration & Final Output**
   - Run your new `/home/user/workspace/manifest.py` script.
   - It should read `/home/user/workspace/artifacts.json`.
   - It should write the migrated v2 manifest (with the dynamically computed checksums) to `/home/user/workspace/final_manifest.json`.

**Requirements for `/home/user/workspace/final_manifest.json`:**
- It must be valid JSON.
- It must match the v2 schema structure produced by the original Ruby script, but with the `"PENDING"` values replaced by the actual checksum strings returned by the `packager` executable.