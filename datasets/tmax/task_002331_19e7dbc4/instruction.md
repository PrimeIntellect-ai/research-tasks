I have a collection of legacy data files in `/home/user/data_lake` that I need to organize and protect from bit-rot before archiving. I want you to build a C++ utility that processes these files, generates a checksum catalog, and creates an Error-Correcting Code (ECC) backup for each file. 

You must use CMake as your build system and dependency manager. Your project should be created in `/home/user/tmr_tool`.

Here are the requirements:

1. **Dependency Management**:
   - Write a `CMakeLists.txt` in `/home/user/tmr_tool`.
   - Ensure the system has `zlib` installed (you may need to install `zlib1g-dev` via `apt-get`). Link against it for CRC32 calculation.
   - Use CMake's `FetchContent` to download and integrate `RapidCheck` (https://github.com/emil-e/rapidcheck.git) for property-based testing.

2. **Error-Correcting Code (TMR)**:
   - Implement a simple Triple Modular Redundancy (TMR) encoder and decoder in C++.
   - **Encode**: For every byte in the input data, output the exact same byte 3 times in a row.
   - **Decode**: For every 3-byte block in the input data, return the majority byte (e.g., if the block is `[0x41, 0x41, 0x42]`, decode to `0x41`).

3. **Property-Based Testing**:
   - Create a test executable named `tmr_test` using RapidCheck.
   - Write a property test that verifies: for any arbitrary `std::vector<uint8_t>`, if you encode it using your TMR encoder, randomly corrupt *at most one* byte in each 3-byte block, and then decode it, the result exactly matches the original `std::vector<uint8_t>`.
   - Run the test suite and redirect its output to `/home/user/test_results.log`.

4. **Data Processing Utility**:
   - Create a main executable named `tmr_process`.
   - When run as `./tmr_process /home/user/data_lake`, it must recursively find all `.dat` files in the given directory.
   - For each `.dat` file:
     a) Calculate its CRC32 checksum using `zlib`.
     b) Create a TMR-encoded backup file by appending `.tmr` to the original file path (e.g., `subdir/file.dat.tmr`).
   - After processing all files, the utility must write a report to `/home/user/report.csv`.
   - The CSV must contain the relative path of the file (relative to `/home/user/data_lake`) and its CRC32 checksum in lowercase 8-character hex format. 
     Example row: `financials/2004.dat,0a1b2c3d`

Compile your project, run your tests to generate `test_results.log`, and then run `tmr_process` on the `/home/user/data_lake` directory to generate the `.tmr` files and `report.csv`.