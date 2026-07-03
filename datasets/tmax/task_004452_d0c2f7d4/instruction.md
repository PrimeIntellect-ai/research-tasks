You are the release manager for a new distributed system. You are trying to build the configuration filtering tool, but the build environment is broken and the filtering logic is incomplete.

Your task is to fix the build, complete the C++ implementation of the configuration filter, and ensure it correctly separates valid (clean) deployment configurations from malicious or invalid (evil) ones.

Here are the requirements:
1. Extract constraints from the deployment manifest image located at `/app/deploy_info.png`. You will need to extract the `MIN_VERSION` and `WS_PORT` from this image.
2. The CMake project in `/app/` builds the `config_filter` tool. However, it currently fails to link because it depends on a shared library `libasm_checker.so` which is not being built. 
3. You must manually compile the provided assembly file `/app/src/asm_checker.s` into a shared library `libasm_checker.so`, place it in `/app/lib/`, and fix `/app/CMakeLists.txt` to correctly link against it.
4. Complete the C++ program `/app/src/main.cpp`. It must accept a single argument: the path to a JSON configuration file.
5. The C++ program must deserialize the JSON file. A valid (clean) config must satisfy ALL of the following:
   - The `version` field must be a valid Semantic Version string that is GREATER THAN OR EQUAL TO the `MIN_VERSION` found in the image.
   - The `ws_endpoint` field must be a valid WebSocket URL starting with `ws://secure.local:` and ending with the exact `WS_PORT` found in the image.
   - The JSON object contains a `magic_code` (integer). You must pass this integer to the external assembly function `int verify_magic(int)`. The function returns 1 if valid, 0 if invalid. Valid configs must have a valid magic code.
6. The `config_filter` executable must exit with code `0` for clean configs, and exit with code `1` for evil configs.

Once you have built the executable at `/app/build/config_filter`, test it. We have provided two directories of test cases:
- `/app/clean/`: Contains only valid configurations.
- `/app/evil/`: Contains configurations that fail one or more of the rules above.

Your final executable must be located at `/app/build/config_filter`. It will be evaluated against a hidden adversarial corpus following the exact same rules.