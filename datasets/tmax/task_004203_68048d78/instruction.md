You are an integration developer troubleshooting an API data processing pipeline. The pipeline involves a C-based data processor and a Python test suite, both of which are currently broken.

Your objectives:

1. **Fix the Data Processor Build**: 
   Navigate to `/home/user/processor/`. The `Makefile` there is currently failing due to syntax errors. Fix the `Makefile` and compile the C program. The resulting executable must be located at `/home/user/processor/processor`.

2. **Debug the Processor Logic**:
   The `processor.c` program has a logic bug in how it transforms numeric characters. We have provided a reference binary at `/app/oracle_processor`. You must modify `processor.c` so that its standard output strictly matches the `oracle_processor` for any standard input. Ensure you recompile the binary after fixing the code.

3. **Extract API Version**:
   We received an image of the target environment's configuration at `/app/api_version.png`. Extract the version string from this image (it will be in the format `VERSION: X.Y.Z`). Tesseract OCR is available on the system.

4. **Semantic Versioning and Patching**:
   Read the list of supported API versions in `/home/user/versions.txt`. Write a Python script to determine the highest version from this list that is less than or equal to the version you extracted from the image, using proper semantic version comparison.
   
   Once you have identified this version, find the corresponding patch file in `/app/patches/` (named `fix_imports_<version>.patch`). Apply this patch to the Python test suite located in `/home/user/api_tests/`. The test suite currently fails due to an import ordering issue, which the correct patch will resolve.

5. **Verify Tests**:
   Run `pytest /home/user/api_tests/` to confirm that the test suite now passes.

Ensure the final patched test suite is saved in `/home/user/api_tests/` and the corrected, compiled C executable is at `/home/user/processor/processor`.