You are a mobile build engineer maintaining our CI/CD pipelines. We recently migrated our pipeline to a lightweight Alpine Linux runner that only has Bash and standard coreutils installed. 

Previously, we used a Go program (`/home/user/collatz_sum.go`) to generate a unique mathematical build ID based on the Collatz conjecture for a given range of build numbers. The Go program used concurrency to calculate the sum of the number of Collatz steps for all integers from A to B (inclusive).

Since Go is no longer available in the new CI environment, you need to translate this numerical algorithm into a pure Bash script.

Please create a Bash script at `/home/user/ci_build_id.sh` that:
1. Takes two integer arguments, A and B (e.g., `./ci_build_id.sh 10 20`).
2. Calculates the sum of the Collatz stopping times (number of steps to reach 1) for all integers in the range [A, B] inclusive.
3. Outputs ONLY the final sum to standard output.
4. Uses only Bash built-ins and standard coreutils (like `seq`, `awk`, `bc`, etc.).
5. Is executable.

For reference, the Collatz sequence rules are:
- If n is even, the next number is n / 2.
- If n is odd, the next number is 3n + 1.
- The sequence stops when n = 1.
The "number of steps" is how many transitions it takes to reach 1.

The original Go program will be present in `/home/user/collatz_sum.go` for your reference.