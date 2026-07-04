Hey, we have an urgent issue with our Go packet parser. Last night, one of our production containers crashed randomly, and this morning our CI pipeline started failing on the fuzz testing step. I need you to debug this failing build and fix the root cause.

Here is what you need to do:
1. Inspect the container logs located in `/home/user/logs/`. You will find logs from multiple nodes. Find the log file that contains the panic stack trace.
2. Identify the exact hex payload that caused the production crash from the log file. Write this exact hex string to `/home/user/crash_payload.txt`.
3. The crashing code is in `/home/user/project/parser.go`. Analyze the traceback and the code. There is a bug when parsing a malformed TLV (Type-Length-Value) packet that causes a slice bounds out of range panic.
4. Fix the bug in `/home/user/project/parser.go`. When the parsed length exceeds the available data, the function should return the error `errors.New("invalid length")` instead of panicking.
5. Verify your fix by running the fuzz tests in the project directory (`/home/user/project/`). The test command `go test -fuzz=FuzzParsePacket -fuzztime=2s` should pass without any panics.

Please get the code fixed and the payload identified!