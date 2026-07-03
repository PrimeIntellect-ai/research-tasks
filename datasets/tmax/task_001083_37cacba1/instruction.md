You are a build engineer migrating a legacy artifact tracking system to a new gRPC/Protobuf-based infrastructure. 

Currently, our build system outputs legacy text files representing state transitions of artifacts. You need to parse these files, construct a protobuf representation, and serialize the parsed artifacts to disk.

Here are your tasks:

1. **Define the Protobuf Schema:**
   Create a file at `/home/user/artifacts/build_artifact.proto` with the following specifications:
   - Syntax: `proto3`
   - Package: `buildsystem`
   - Enum `BuildState`: `UNKNOWN_STATE = 0`, `INIT = 1`, `COMPILED = 2`, `PACKAGED = 3`, `FAILED = 4`
   - Message `Artifact`:
     - `string name = 1;`
     - `repeated string dependencies = 2;`
     - `string artifact_hash = 3;`
     - `BuildState final_state = 4;`

2. **State Machine Parser & Protobuf Serialization:**
   Write a Python script `/home/user/artifacts/migrate.py` that parses `/home/user/artifacts/legacy_build.log`.
   The log file format is:
   ```
   BEGIN_ARTIFACT <name>
   STATE <state_name>
   DEPENDS <dependency_name>
   HASH <hash_value>
   END_ARTIFACT
   ```
   - Use a state machine approach to parse each artifact block.
   - An artifact can have multiple `STATE` lines; `final_state` should be the *last* state recorded before `END_ARTIFACT`.
   - `DEPENDS` lines add to the dependencies list (in order of appearance).
   - Once an `END_ARTIFACT` is reached, serialize the `Artifact` protobuf message to binary format and save it as `/home/user/artifacts/out/<name>.bin`.
   - Ensure you compile the protobuf file to Python (`protoc`) before writing your script.

3. **Unit Testing:**
   Write a pytest test suite in `/home/user/artifacts/test_migrate.py` that tests your parser logic on at least one mock string.

4. **Execution and Verification:**
   - Create the directory `/home/user/artifacts/out/` if it doesn't exist.
   - Run your test suite.
   - Run your `migrate.py` script to generate the `.bin` files.
   - Finally, create a log file at `/home/user/artifacts/completion.log` containing exactly one line per generated `.bin` file in the format: `<name>.bin: <sha256_hash_of_bin_file>` (sorted alphabetically by filename).