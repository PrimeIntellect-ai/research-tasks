You are a developer taking over a broken multi-file C++ project located in `/home/user/api_processor`. The project is meant to act as a mock REST/GraphQL API data processor. It reads serialized JSON requests (representing old schema Data Objects) from standard input (`stdin`), migrates them to a new schema, and writes the serialized JSON responses to standard output (`stdout`).

Currently, there are two major issues:
1. The build script (`/home/user/api_processor/build.sh`) is broken and fails to compile the project. You need to fix the build configuration so that running `./build.sh` produces an executable at `/home/user/api_processor/build/processor`.
2. The schema migration logic in `src/migration.cpp` is incomplete. The exact rules for migrating from Schema V1 to Schema V2 were documented in a video recording of a design meeting, which is provided to you at `/app/migration_rules.mp4`. 

Your tasks are:
1. Fix the build system so the C++ project compiles successfully.
2. Use `ffmpeg` to extract frames from `/app/migration_rules.mp4`.
3. Analyze the extracted frames to find the schema migration mapping rules (e.g., which V1 fields map to which V2 fields, and any data type conversions).
4. Implement the test fixture and migration logic in `src/migration.cpp`. The program must read a V1 JSON string from `stdin` on a single line, apply the migration rules exactly as shown in the video, and output the resulting V2 JSON string on a single line to `stdout`.

Constraints:
- Do not use external libraries other than standard C++17 libraries. You can assume a basic single-header JSON library is already included in `include/json.hpp`.
- Your final executable must be located precisely at `/home/user/api_processor/build/processor`.
- The processor must exit with code 0 after processing one line of standard input.