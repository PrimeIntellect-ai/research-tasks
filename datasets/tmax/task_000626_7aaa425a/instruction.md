I need you to help me with our localization data processing pipeline. As a localization engineer, I process large streams of translation updates from our vendors. These arrive in JSON-lines format. Recently, our custom C++ JSON parser stopped working correctly.

First, fix our vendored C++ JSON parsing library located at `/app/vendored/tiny-json-lines`. There is a known issue where it crashes or silently drops characters when it encounters valid Unicode escape sequences (e.g., `\u00A9` or `\u20AC`). You need to patch `parser.cpp` inside the vendored package so it correctly interprets and converts these unicode escape sequences into standard UTF-8 characters. The build system (Makefile) in that directory also has a minor misconfiguration pointing to the wrong compiler flag (`-std=c++11` instead of `-std=c++17`); fix that and ensure the static library `libtinyjson.a` builds successfully.

Second, create a C++ tool at `/home/user/mask_loc.cpp` that links against this fixed `libtinyjson.a`. This tool will act as a multi-stage pipeline worker. It should read a single JSON object from standard input. The JSON object will have this structure:
`{"loc_key": "string", "text": "string", "user_id": 12345, "confidence_score": 0.95}`

Your tool must perform the following transformations:
1. Parse the JSON.
2. Data Masking (Mathematical): Obfuscate the `user_id` by applying a deterministic transformation: `masked_id = (user_id * 6364136223846793005ULL + 1442695040888963407ULL) % 4294967296ULL`.
3. Pipeline Transformation: Round the `confidence_score` down to the nearest multiple of `0.1` (e.g., `0.95` becomes `0.9`, `0.89` becomes `0.8`).
4. Output a strictly formatted JSON string to standard output with the keys in alphabetical order, exact spacing, and no trailing newline:
`{"confidence_score": <val>, "loc_key": "<val>", "masked_id": <val>, "text": "<val>"}`

Compile your tool to `/home/user/mask_loc`.

Finally, orchestrate this using a Makefile DAG in `/home/user/Makefile` that has three targets:
- `build`: compiles `/home/user/mask_loc` linking the vendored library.
- `run`: reads `input.jsonl` and writes the processed output to `output.jsonl`.