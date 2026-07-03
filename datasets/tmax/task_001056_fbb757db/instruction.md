You are a systems programmer working on a Go-based web security service. The service verifies secure access tokens using an optimized C library. However, the build is currently failing due to a C library linking issue. The C code calls an external assembly routine `check_sig` which is missing, causing an "undefined reference" error during `go build`.

Your workspace is located at `/home/user/workspace/auth`.
The main file is `/home/user/workspace/auth/main.go`, which contains:
```go
package main

/*
extern int check_sig(char* msg);
int validate_token(char* token) {
    return check_sig(token);
}
*/
import "C"
import (
    "fmt"
    "net/http"
)

func Validate(token string) bool {
    return C.validate_token(C.CString(token)) == 1
}

func AuthHandler(w http.ResponseWriter, r *http.Request) {
    token := r.URL.Query().Get("token")
    if Validate(token) {
        w.WriteHeader(http.StatusOK)
        w.Write([]byte("OK"))
    } else {
        w.WriteHeader(http.StatusUnauthorized)
    }
}

func main() {
    http.HandleFunc("/auth", AuthHandler)
    http.ListenAndServe(":8080", nil)
}
```

Perform the following tasks:
1. Fix the linking issue by writing a minimal x86_64 GNU assembly file named `/home/user/workspace/auth/mock.S`. This file must define the global symbol `check_sig` as a function that always returns `1` (simulating a valid signature).
2. Write a Go test suite in `/home/user/workspace/auth/main_test.go`. The test must use `net/http/httptest` to set up a test fixture for `AuthHandler`.
3. In your test, use Go concurrency patterns to spawn exactly 100 goroutines. Each goroutine should make a simulated HTTP GET request to `/auth?token=test` concurrently. 
4. Use a channel to collect the status codes from all 100 requests. 
5. Count the total number of `http.StatusOK` (200) responses received.
6. Write this total count as a plain text string (e.g., `100`) to `/home/user/workspace/auth/result.txt`.
7. Run your test to ensure it creates the `result.txt` file.

Do not modify `main.go`. Ensure your assembly file acts as a valid CGO drop-in mock.