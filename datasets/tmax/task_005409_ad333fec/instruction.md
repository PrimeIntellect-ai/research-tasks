As a QA engineer, you need to set up our new Go-based Web Application Firewall (WAF) testing environment and migrate our legacy Python rules.

We have a vendored WAF engine package located at `/app/gowaf` (version 1.0.0). However, the repository has a few issues that prevent it from compiling:
1. The `Makefile` has a syntax/typo error.
2. The `parser.go` file has a missing import.
You must fix these issues so the package can be compiled and imported.

Next, you need to translate our legacy Python WAF filter into Go. The legacy filter is located at `/home/user/legacy_waf.py`. 
Your Go implementation must:
1. Import and utilize our fixed local module `/app/gowaf` (you can use `go mod edit -replace` to point to the local directory). The `gowaf` package provides a `NormalizePayload(input string) string` function.
2. Accurately translate the detection logic from the Python script to Go.
3. Be compiled into a binary at `/home/user/waf_filter`.

Your compiled binary `/home/user/waf_filter` will act as a detector. It must accept a single command-line argument representing a directory path. It should iterate through all files in that directory, process their contents, and print the classification for each file to standard output in the exact format:
`<filename>: EVIL`
or
`<filename>: CLEAN`

We have provided two corpora for testing:
- `/home/user/corpus/evil/`: Contains malicious payloads (must be classified as EVIL).
- `/home/user/corpus/clean/`: Contains safe payloads (must be classified as CLEAN).

To succeed, your detector must achieve a 100% pass rate: 100% of the evil corpus rejected (flagged EVIL) and 100% of the clean corpus preserved (flagged CLEAN). Write your Go source code to `/home/user/waf.go` and build the binary to `/home/user/waf_filter`.