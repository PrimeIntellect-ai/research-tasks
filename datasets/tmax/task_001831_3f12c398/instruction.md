You are acting as a support engineer collecting diagnostics. We rely on a custom Go-based CLI tool called `log-stitcher` to parse, reconstruct, and chronologically sort container logs across our microservices. 

Recently, the tool started dropping specific log entries, causing incomplete diagnostic timelines. The source code is provided as a vendored git repository in `/app/log-stitcher`. 

Your objectives:
1. **Find the Regression:** The bug was introduced somewhere after the `v1.1.0` tag. Use git bisection in the `/app/log-stitcher` repository to identify the exact commit that broke the container log timestamp parser.
2. **Fix the Code:** Once you identify the bad commit, diagnose the Go code (likely an issue with timezone parsing, concurrent map writes, or fractional second handling in `parser.go`) and fix it.
3. **Build the Binary:** Compile your fixed version of the tool. You must place the final compiled executable exactly at `/home/user/fixed-stitcher`.

The compiled binary must take a stream of raw container logs via standard input and output the perfectly reconstructed timeline to standard output. Its behavior must be bit-exact equivalent to our reference implementation for all valid and edge-case log formats.

Do not use external network resources to download new dependencies; the `vendor` directory is already populated and configured.