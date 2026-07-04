You are an open-source maintainer reviewing a recent Pull Request for the `api-gateway-core` project. This package provides an ultra-fast REST and GraphQL API gateway for request validation, rate limiting, and payload encoding verification. To achieve maximum throughput, the core validation and rate-limiting logic is implemented as a native C++ addon for Node.js.

A contributor submitted a PR to add robust Base64 encoding validation and advanced rate limiting. However, the PR is broken in multiple ways:
1. The build system configuration for the native addon was accidentally modified and no longer compiles.
2. After patching the build locally, users reported that the API throughput completely tanked. The new character encoding validation logic in the C++ core seems to have a severe performance regression, likely caused by an inefficient algorithm blocking the Node.js event loop.

Your task is to fix this broken PR:
1. Navigate to the vendored package at `/app/api-gateway-core`.
2. Fix the build configuration so that `npm run build` (which invokes `node-gyp`) completes successfully.
3. Analyze the C++ native addon source code (`src/validator.cpp`) and refactor the `validatePayload` function. The current implementation for validating the Base64 encoding is incredibly slow for large payloads. Optimize it to be at least O(N) so it can handle large request bodies without stalling the server.
4. Once compiled and optimized, start the server and use the provided `npm run benchmark` command to evaluate the throughput.
5. Save the exact console output of the benchmark script to `/app/benchmark_results.txt`. 

To successfully complete this task, the native addon must compile, all logical checks must remain intact (it must still correctly reject invalid Base64 payloads), and the optimized C++ validation function must pass the strict performance threshold defined in the project's continuous integration verifier.