You are a release manager preparing a new high-performance deployment gateway. We are migrating our deployment validation logic from Python to C to handle high-throughput edge environments.

Your task is to build the new deployment gateway in C (`/home/user/gateway.c`) that processes a batch of deployment requests, applies rate limiting, compares semantic versions, and serializes the approved requests into a binary format.

**Phase 1: Code Translation**
In `/home/user/legacy_semver.py`, you will find our custom semantic version comparison logic. It handles basic `X.Y.Z` format and specific pre-release tags (`alpha`, `beta`, `rc`, `final`). 
Translate this exact logic into a C function `int compare_versions(const char* v1, const char* v2)` within your `gateway.c` file. It should return -1 if v1 < v2, 0 if v1 == v2, and 1 if v1 > v2.

**Phase 2: Request Validation and Rate Limiting**
Your C program must read a JSON Lines file located at `/home/user/requests.jsonl`. 
Each line has the following format:
`{"env_id": <int>, "timestamp": <long>, "current_version": "<string>", "target_version": "<string>"}`

To process each request, implement the following checks:
1. **Version Validation:** Use your translated `compare_versions` function. The deployment is only valid if `target_version` is strictly greater than `current_version`.
2. **Rate Limiting:** A maximum of 2 *valid* (version-approved) deployments are allowed per `env_id` within any rolling 60-second window. The timestamps in the file are Unix epochs and are chronologically ordered. If a request is version-approved but violates the rate limit, it is rejected.

You may use `libjansson` for JSON parsing (you will need to install `libjansson-dev` via apt).

**Phase 3: Serialization**
If a request passes both version validation and rate limiting, it is APPROVED. 
Your C program must serialize all APPROVED requests sequentially into a binary file at `/home/user/approved.bin` with the following tight-packed binary format (Little Endian):
- `env_id` (uint32_t)
- `timestamp` (uint64_t)
- `target_version_len` (uint8_t) - length of the target version string, excluding null terminator
- `target_version` (char array) - the exact bytes of the target version string (NO null terminator)

**Instructions:**
1. Review `/home/user/legacy_semver.py`.
2. Write `/home/user/gateway.c`.
3. Compile it to `/home/user/gateway` using `gcc -o gateway gateway.c -ljansson`.
4. Run your compiled gateway program. It must read `/home/user/requests.jsonl` and output `/home/user/approved.bin`.

Ensure your C code matches the exact logic of the Python script for version comparison.