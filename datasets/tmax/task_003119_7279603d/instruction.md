You are acting as a DevOps engineer investigating a severe performance degradation in our internal log analysis tool, `fast-log-grep`. 

Our CI pipeline recently deployed a new version of the tool, and our log ingestion pipeline is now backing up. The tool is supposed to quickly filter and extract query results from our custom structured log format.

Here is what we know:
1. The source code for the tool is located in a Git repository at `/app/fast-log-grep`.
2. The current `main` branch HEAD is exhibiting the performance issue. We know that a few days ago, the parsing was lightning fast.
3. The tool relies on a proprietary compiled shared library located at `/app/lib/libqueryengine.so` for the core matching logic. The source for this library is not available, but it was updated around the same time.
4. The logs contain occasional malformed edge-case lines (e.g., mismatched brackets or escaped quotes in the metadata fields) which seem to trigger the bug.
5. The performance bug severely impacts processing speed, likely due to an inefficient format parsing implementation or an incorrect API call to the `libqueryengine.so` library introduced in a recent commit.

Your task:
1. Clone or investigate the repository at `/app/fast-log-grep`.
2. Identify the regression commit.
3. Use whatever binary inspection tools you need (e.g., `nm`, `objdump`) to understand the exported symbols of `/app/lib/libqueryengine.so` if the regression involves the library integration.
4. Fix the C++ source code to handle the format edge-cases correctly and efficiently, restoring the original performance without breaking the query accuracy.
5. Recompile the tool using standard `CMake` and `make`. The final executable must be located at `/app/fast-log-grep/build/fast-log-grep`.

The automated test will evaluate the performance of your compiled executable against a massive 50MB held-out log file. Your patched version must execute the test query in under 0.5 seconds.