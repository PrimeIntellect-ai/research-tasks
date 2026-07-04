You are a Site Reliability Engineer (SRE) investigating recurring outages in our custom Go-based uptime monitoring service (`healthd`). The service randomly crashes with a stack overflow panic. 

We managed to capture a raw memory dump of the crashed process's heap right before a crash, located at `/app/crash.dmp`. 

Your tasks are:
1. **Memory Dump Analysis & String Extraction:** Analyze `/app/crash.dmp` using standard shell built-ins or coreutils (e.g., `strings`, `grep`) to find the malicious tag that caused the crash. The tag always follows the format `X-Malicious-Tag: <data>`. Write the exact extracted `<data>` value to `/home/user/malicious_tag.txt`.
2. **Fuzz Testing:** Write a Go fuzz test in `/app/healthd/parser_test.go` that targets the `ParseTags(input []byte) string` function. The fuzzer should demonstrate the vulnerability by causing a stack overflow or infinite loop.
3. **Loop Termination Fixing:** Fix the bug in `/app/healthd/parser.go`. The parsing function has a recursive loop that reads a length header. Due to an architectural integer type conversion (treating a parsed length as a signed 8-bit integer), large lengths overflow to negative numbers, bypassing the termination condition and causing infinite recursion. Fix this so the function handles invalid lengths gracefully without crashing.
4. **Service Composition:** 
   - Start the mock target service (`go run /app/mock_target/main.go`) which listens on `127.0.0.1:8081`.
   - Compile and start the fixed `healthd` service (`/app/healthd/main.go`), ensuring it listens on `127.0.0.1:8080`.

Ensure both services are running in the background when you complete your turn. Do not modify the mock target service.