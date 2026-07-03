You are a platform engineer maintaining the CI/CD pipeline infrastructure for your company. We have a Go-based Build Cache Node service that caches build artifacts. Currently, it has performance issues, lacks architectural flexibility, and needs strict rate limiting to prevent abuse from rogue CI jobs. 

Your workspace is located at `/home/user/cache-node`.

Here are your tasks:

1. **Service Configuration & Integration (Nginx + Go + Redis)**
   We are running a multi-service architecture. Redis is already running on port `6379`. Nginx is running but needs to be configured. 
   - Modify the Nginx configuration at `/etc/nginx/sites-available/default` (or create a new one and symlink to `sites-enabled`) so that all requests to `http://localhost:8080/api/` are proxy-passed to the Go service running on `http://localhost:9000`.
   - Start or reload Nginx.

2. **CGO Performance Optimization**
   Our artifact chunking mechanism uses a custom hash algorithm. The pure Go implementation in `/home/user/cache-node/hash_go.go` is too slow for large artifacts. 
   - We have provided a C skeleton in `/home/user/cache-node/hash.c`. Implement the same logic as `hash_go.go` in C.
   - Wire it up in `/home/user/cache-node/hash_cgo.go` using `cgo`.
   - Use Go build tags to ensure the CGO version is only used on `linux,amd64`. On other platforms, it should fallback to the pure Go version.
   - Your CGO implementation must be highly optimized. An automated benchmark will compare the CGO version against the pure Go reference. You must achieve a **speedup of at least 4.0x** (CGO implementation must be at least 4 times faster than the Go fallback).

3. **Expression Parsing for Cache Rules**
   In `/home/user/cache-node/rules.go`, implement the `EvaluateRule(expr string, branch string, size int) (bool, error)` function. It must parse and evaluate simple string rules like:
   `branch == "main" && size < 50000`
   Supported operators: `==`, `!=`, `<`, `>`, `&&`, `||`.
   This determines if an artifact should be cached.

4. **Rate Limiting with Redis**
   In `/home/user/cache-node/limit.go`, implement an IP-based rate limiter using the `github.com/go-redis/redis/v8` package. Limit uploads to 5 requests per second per IP. Return an HTTP 429 status code if the limit is exceeded.

5. **Final Integration**
   - Build your Go binary for `linux/amd64` (with CGO enabled).
   - Start the Go service so it listens on port 9000.
   - Leave the services (Redis, Nginx, Go App) running in the background.

To test your work, you can run `go test -bench .` in the directory, and you can send requests to `http://localhost:8080/api/upload` to ensure Nginx properly routes traffic to your Go service and Redis tracks the rate limits.