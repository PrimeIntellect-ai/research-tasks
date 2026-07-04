You are an on-call engineer who just got paged at 3 AM. The downstream authentication service is failing because our C++ log data processor is outputting corrupted tokens. Additionally, the service needs a static secret key to verify the tokens, but it seems the key was recently accidentally removed from the codebase.

You need to investigate the repository located at `/home/user/data_pipeline` and fix the issues so the pipeline can be restored.

Here is what you need to do:

1. **Secret Recovery**: A secret key was previously hardcoded in `config.h` but was removed in a recent commit. Find this secret key in the git history and write it exactly as it appeared (just the value itself, no quotes or variable names) to `/home/user/secret.txt`.

2. **Fix the Parser**: The data processing program `parser.cpp` reads `/home/user/data_pipeline/logs.txt` and extracts authentication tokens to `output.txt`. It currently has a boundary condition / off-by-one error in its string extraction logic, which causes it to extract malformed tokens (they include an extra character or are missing a character). Fix the substring extraction logic in `parser.cpp` so it extracts *only* the exact token (e.g., `tk_abc123`).

3. **Intermediate State Tracing**: To ensure the parser is working correctly and for future auditing, modify `parser.cpp` to append a trace of the token lengths to `/home/user/trace.log`. For every token parsed, it should write a line exactly in this format: `Token length: <length>` (where `<length>` is the integer length of the extracted token).

4. **Execution**: Compile your fixed `parser.cpp` into an executable named `parser` in the same directory, and run it. Ensure that `/home/user/data_pipeline/output.txt` contains the correctly parsed tokens, one per line.

Make sure your final files (`/home/user/secret.txt`, `/home/user/trace.log`, and `/home/user/data_pipeline/output.txt`) are correct. You have standard bash tools, git, and g++ at your disposal.