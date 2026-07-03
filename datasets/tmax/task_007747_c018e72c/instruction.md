You are an expert DevOps engineer and Go developer. We are facing a critical issue in our log aggregation pipeline. 

Our custom log processor, written in Go, parses incoming logs from various microservices. However, it periodically crashes with an out-of-bounds panic when processing certain log files, causing the entire pipeline to halt. This seems to happen when the log messages contain specific malformed strings (we suspect it has something to do with spaces inside unclosed quotes, similar to how poorly written shell scripts break on filenames with spaces).

You have been provided with the source code for the log processor in `/home/user/log_processor`.

Here is what you need to do to fix the pipeline:

1. **Dependency Conflict Resolution**: We recently tried to update the project, but now it fails to build. The `go.mod` file in `/home/user/log_processor` has a dependency conflict involving `github.com/sirupsen/logrus` and `github.com/google/uuid`. Resolve this conflict so that `go build` runs successfully without modifying the application's source code imports.

2. **Fuzz Testing & State Tracing**: To definitively identify the edge case causing the panic, write a Go fuzz test (`FuzzParseLogLine`) in a new file `/home/user/log_processor/parser_test.go`. The fuzzer should test the `ParseLogLine(line string)` function in `parser.go`. Use this to trace and reproduce the panic.

3. **Fix the Bug**: Once you understand the root cause from the fuzzer, modify `ParseLogLine` in `/home/user/log_processor/parser.go` to safely handle these edge cases without panicking. It should return an error instead of panicking when it encounters an unclosed quote.

4. **Process the Logs**: After fixing the code, recompile the tool (`go build -o processor`). Run the tool to process the raw logs located at `/home/user/raw.log`. 

5. **Generate Final Output**: The tool takes an input file and an output file as arguments: `./processor /home/user/raw.log /home/user/processed_logs.json`. Run this command. Ensure the tool completes successfully and writes the parsed JSON to `/home/user/processed_logs.json`.

**System State & Constraints:**
- The Go project is in `/home/user/log_processor`.
- The raw log file is at `/home/user/raw.log`.
- Do not change the function signature of `ParseLogLine(line string) (map[string]string, error)`.