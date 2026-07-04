You are a build engineer managing our core artifact repository infrastructure. Our system relies on a fast, C++ based URL routing and parameter parsing utility. However, the current artifact router (`/home/user/src/router.cpp`) has several issues:
1. It contains severe memory safety bugs (buffer overflows and memory leaks) when parsing long URLs or malformed query parameters.
2. It is missing a crucial mathematical hashing step for the parsed paths, which determines the backend storage shard.

We have received an audio memo from the lead architect detailing the exact mathematical hashing algorithm required for the routing paths. The audio file is located at `/app/artifact_routes.wav`.

Your task is to:
1. Transcribe or listen to `/app/artifact_routes.wav` to obtain the exact mathematical formula for the path hash.
2. Debug and repair the C++ memory safety issues in `/home/user/src/router.cpp`. Use tools like Valgrind or AddressSanitizer to ensure there are zero memory leaks and no undefined behavior (UB) on malformed inputs.
3. Implement the mathematical hash logic dictated by the audio snippet. The router should extract the URL path (everything before `?`) and apply the hash.
4. Compile your final, optimized, and memory-safe C++ implementation to the executable path `/home/user/router_fixed`. 

The binary `/home/user/router_fixed` must accept exactly one command-line argument (the URL) and output exactly the following format to standard output:
```
Path: <parsed_path>
Hash: <computed_integer_hash>
Params: <key1>=<value1>;<key2>=<value2>;
```
If there are no parameters, print `Params: none`.
Ensure your parameter parsing handles standard `&` separation and correctly manages memory. 

Your executable will be aggressively fuzz-tested against a secret reference oracle to ensure absolute bit-exact output equivalence and strict memory safety.