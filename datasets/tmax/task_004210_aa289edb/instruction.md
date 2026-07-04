You are a platform engineer maintaining the CI/CD pipelines for a data processing team. A step in the pipeline is frequently failing with an Out of Memory (OOM) error when processing large server log files. 

The problematic Go code is located in `/home/user/logprocessor/main.go`. It currently reads a large newline-delimited JSON (NDJSON) file entirely into memory before filtering and uploading error events.

Your task is to optimize, test, and profile this codebase:

1. **Package & Dependency Management**:
   Navigate to `/home/user/logprocessor`. Initialize a Go module named `example.com/logprocessor`. 

2. **Memory Optimization**:
   Refactor the `ProcessLogs(filePath string, uploader Uploader) (int, error)` function in `main.go`. 
   Instead of reading the entire file into memory using `os.ReadFile` or `ioutil.ReadFile`, refactor it to stream the file line-by-line using standard Go streaming mechanisms (e.g., `bufio.Scanner` or `json.Decoder`). 
   The function must extract the `status` and `message` fields. If the `status` is exactly `"ERROR"`, it must call `uploader.Upload(status, message)`. It should return the total count of successfully uploaded ERROR logs.

3. **Test Fixtures & Mocking**:
   Create a test file `/home/user/logprocessor/main_test.go`.
   Write a unit test for `ProcessLogs`. You must implement a mock `Uploader` (a struct that implements the `Uploader` interface) to track the calls without making actual network requests. Provide a small dummy NDJSON file or use an in-memory test fixture for the test. Ensure `go test` passes.

4. **Memory Profiling**:
   Modify the `main()` function in `main.go` to:
   - Instantiate a mock/dummy uploader.
   - Run `ProcessLogs` on `/home/user/logprocessor/data.jsonl`.
   - Start a memory profile using `runtime/pprof` before processing, and write the heap profile to `/home/user/logprocessor/mem.pprof` immediately after processing completes.
   - Write the integer count of ERROR logs returned by `ProcessLogs` to a file named `/home/user/logprocessor/result.txt`.

Ensure the final code compiles, the tests pass, the memory profile is generated, and the result file contains the correct integer. You are allowed to use standard CLI tools alongside Go commands.