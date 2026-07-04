You are a mobile build engineer maintaining the CI pipelines for an internal Python tool called `mathparser_mobile`. This package provides a fast C-extension for parsing and evaluating mathematical expressions, which is critical for generating mobile app configuration files dynamically.

Currently, the build pipeline is broken. You have been provided with the source code in `/home/user/mathparser_mobile`. Your goal is to fix the build configuration, successfully compile the C extension, and ensure all property-based tests pass.

Here are the issues you need to resolve:
1. **Semantic Versioning Check Bug:** `setup.py` attempts to verify that the build environment meets a minimum version requirement (version `1.5.0`). However, the version comparison logic is flawed and incorrectly fails when the environment version is `1.10.2`.
2. **Checksum Validation Bug:** Before compiling, `setup.py` validates the SHA256 checksum of `src/ops.h` to ensure file integrity. The validation fails even though the file is unmodified, likely due to how the file is being read or hashed in Python.
3. **Compilation/Linking Error:** Once the setup script runs, the C extension fails to compile/link because it uses mathematical functions from the standard C library, but the math library is not properly linked in the `Extension` definition in `setup.py`.

Your task:
1. Fix the bugs in `/home/user/mathparser_mobile/setup.py`.
2. Build the extension in-place using `python3 setup.py build_ext --inplace`.
3. Run the property-based test suite using `pytest /home/user/mathparser_mobile/test_parser.py`.
4. Once the tests pass successfully, create a file at `/home/user/success.log` containing exactly the text: `BUILD SUCCESS`.

Do not modify the C source code or the test files. Your fixes should be contained entirely within `setup.py`.