You are tasked with fixing and running a polyglot data pipeline for a new build system's telemetry gatherer. The system uses a Go program to concurrently collect build events and encode them into a custom binary format, and a C++ tool to parse this format and generate a readable log. 

Currently, both the Go generator and the C++ parser are broken. 

1. **Fix the Go Generator (`/home/user/generate.go`):**
   The Go program uses goroutines to generate events and send them to a channel, which a consumer writes to `data.bin`. However, the concurrency pattern is flawed: the main function exits before all goroutines finish, and the consumer doesn't cleanly flush. Fix the Go code by correctly using a `sync.WaitGroup` for the producers, closing the channel when they are done, and ensuring the consumer finishes writing before the program exits.

2. **Fix the C++ Parser (`/home/user/parser.cpp`):**
   The C++ program reads `data.bin` using a custom `EventBuffer` data structure. It decodes the custom binary format (where each record is a 1-byte length header `N` followed by `N` bytes of an ASCII string). There are two critical C++ memory safety/Undefined Behavior issues in the `readNext()` function involving buffer allocation, bounds writing, and deallocation. Find and repair them.

3. **Execution & Output:**
   - Compile the Go program and run it to produce `/home/user/data.bin`.
   - Compile the C++ program (e.g., `g++ -O2 /home/user/parser.cpp -o /home/user/parser`).
   - Run the C++ parser on `data.bin` and redirect the standard output to `/home/user/decoded.log`.
   
Sort the output lines alphabetically if they aren't already, but do that by piping the output through `sort` when saving to `decoded.log`.

Ensure `/home/user/decoded.log` contains exactly 50 lines, formatted as `Parsed: Event-<ID>`.