You are acting as a release manager preparing a new deployment for a custom Stack Machine Emulator that exposes a REST API. The engineering team handed over the release candidate in `/home/user/emulator_release`, but it currently fails to compile due to memory ownership and lifetime issues (specifically involving `std::unique_ptr` in C++). 

Additionally, the new release introduces a backward-incompatible schema change for the emulator's saved state files, and you need to perform a schema migration on the existing state files before launching the service.

Your task consists of three parts:

**Part 1: Fix Code and Build**
1. Navigate to `/home/user/emulator_release`. The project contains a `Makefile`, `main.cpp`, `machine.cpp`, and `machine.h`. It uses `httplib.h` and `json.hpp` for the REST API.
2. Run `make`. You will see compilation errors related to copy-constructors and `std::unique_ptr` in `machine.cpp`. 
3. Fix the code. The bugs are caused by attempting to copy a vector of `std::unique_ptr<Instruction>` and returning raw pointers improperly. You must fix these using proper move semantics (`std::move`) or references, ensuring the project compiles successfully and produces the `emulator_server` binary.

**Part 2: Schema Migration**
1. There is a directory of saved state files at `/home/user/states/`. These JSON files currently use Schema V1.
   * V1 Format: `{"stack": [int, int, ...], "pc": int}`
2. The new emulator requires Schema V2. You must migrate all `.json` files in this directory to V2 format.
   * V2 Format: `{"machine_state": {"data_stack": [int, int, ...], "instruction_pointer": int}, "version": 2}`
3. Write a bash script or one-liner to overwrite the V1 files with their V2 equivalents. Keep the original filenames.

**Part 3: Run and Validate**
1. Start the compiled `./emulator_server` in the background. It will bind to `localhost:8080`.
2. The server exposes a `POST /load_and_run` endpoint. It expects a JSON payload matching the V2 schema.
3. Use `curl` to send the contents of the migrated `/home/user/states/state_1.json` to `http://localhost:8080/load_and_run`.
4. Save the HTTP response body exactly as it is received into `/home/user/deployment_log.txt`.

Ensure all code compiles, the server stays running, the migration is exact, and the log file contains the final API response.