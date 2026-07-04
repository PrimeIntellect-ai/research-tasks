You are a developer tasked with fixing a broken C++ project located in `/home/user/project`. This project handles a schema migration from an old legacy UTF-16 data format to a new UTF-8 JSON schema.

Currently, the project is failing on multiple fronts:
1. **Build System & Linking**: The project uses CMake. There is a shared library `encoder` and an executable `migrator_test`. Currently, `migrator_test` fails to link against `libencoder.so` and cannot find it at runtime. You need to fix `/home/user/project/CMakeLists.txt` so that it successfully links the shared library and sets the proper RPATH (or links it correctly) so the test binary can be executed from the `build` directory without manually setting `LD_LIBRARY_PATH`.
2. **Memory Safety & Undefined Behavior**: The function `migrate_record` in `/home/user/project/src/migrator.cpp` has a memory safety bug (an out-of-bounds write or null-termination issue) that causes a segmentation fault when converting the character encoding and migrating the schema. Find and fix the memory safety issue.
3. **Test Fixture**: The test file `/home/user/project/test/test_migrator.cpp` is missing the initialization of the test fixture data. You need to provide the correct UTF-16 mock bytes for the string "Test" (in little-endian, no BOM) in the `setup_mock_data()` function so that the tests pass.

Your final goal is to create a shell script at `/home/user/run.sh` that:
1. Creates a `build` directory in `/home/user/project`.
2. Runs `cmake ..` and `make`.
3. Executes `./migrator_test` from within the `build` directory.
4. Exits with code 0 if all tests pass.

Do not use `sudo`. Ensure all paths and dependencies remain strictly in the `/home/user/project` directory.