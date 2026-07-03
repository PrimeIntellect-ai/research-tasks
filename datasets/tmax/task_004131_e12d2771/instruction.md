You are a support engineer investigating a legacy proprietary mathematical engine. Our service relies on a compiled binary located at `/app/legacy_calc`. Unfortunately, the source code has been lost, and the binary has been stripped. 

Recently, customers have reported that the service randomly crashes and disconnects when certain numbers are sent to it. 

Your task is to:
1. **Diagnose the Crash:** Use interactive debuggers (`gdb`) or syscall tracers (`strace`) to figure out what mathematical condition causes the binary to crash (e.g., a specific hardware exception or memory fault).
2. **Reverse-Engineer the Math:** Deduce the mathematical function `f(x)` the binary is computing for valid integers. 
3. **Build a Reliable Replacement:** Since we cannot patch the binary without the source, you must create a Bash-based TCP service that completely replaces it. 
    - The service must listen on `127.0.0.1:9999`.
    - It must accept newline-terminated integers (one per connection or multiple per connection, handle standard TCP streaming).
    - It must return the correct `f(x)` for **all** inputs, including the ones that normally crash the legacy binary.
    - Write this wrapper entirely in Bash using tools like `socat` or `nc` (a standard `socat TCP-LISTEN:9999,reuseaddr,fork EXEC:/home/user/handler.sh` pattern is recommended).

**Constraints:**
- You must write the replacement logic in Bash (shell built-ins and standard coreutils like `bc` or `awk` are fine).
- Do not attempt to decompile the binary to C code using external AI tools; use dynamic analysis, diffing, and math deduction to figure out the sequence.
- Ensure your Bash TCP server is running continuously in the background by the time you finish your turn.