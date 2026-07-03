You are acting as a capacity planner analyzing resource usage across our internal Git repositories. We have a custom Go-based tool called `cap-analyzer` that calculates deduplicated filesystem usage, but the currently vendored version is broken and extremely slow when processing heavily symlinked directory structures.

Your tasks are as follows:

1. **Fix the Vendored Package:**
   The source code for `cap-analyzer` is located at `/app/cap-analyzer`. It contains a deliberate bug in `walker.go` where it infinitely follows symlinks, causing exponential slowdowns or crashes. Fix the Go code so it tracks visited inodes and skips already visited files/directories, ensuring it evaluates the actual disk footprint accurately.
   Build the fixed binary and place it at `/home/user/bin/cap-analyzer`.

2. **Structure Management & Git Hook:**
   We have a bare Git repository at `/home/user/repos/data-model.git`. We need to automatically run this capacity analysis every time new code is pushed.
   Create a `post-receive` hook in this repository that executes `/home/user/bin/cap-analyzer --target /home/user/repos/data-model.git`.
   The output of the analyzer must be appended to `/home/user/logs/capacity.log` in the format: `[TIMESTAMP] SIZE_IN_BYTES`.

3. **Network & Routing constraint:**
   To ensure the capacity logs are accessible to our metrics scraper, bind a lightweight local HTTP file server on `127.0.0.1:8080` serving the `/home/user/logs/` directory. Route any requests intended for `10.0.0.99` to `127.0.0.1` locally (simulate this by adding a local route or iptables rule, but since you don't have root, simply start the server on `127.0.0.1:8080` and ensure it responds).

Our automated tests will push a large, highly linked repository to `data-model.git` and measure the execution time and accuracy of the resulting log. Your fixed Go binary must achieve a significant speedup over the baseline and report the correct byte size.