You are acting as a Database Reliability Engineer (DBRE) responsible for our automated backup validation pipeline. 

As part of our disaster recovery checks, we export the execution plans (in JSON format) of several complex analytical views and scheduled backup queries to ensure that schema changes haven't introduced catastrophic performance regressions (e.g., massive Cartesian products or unoptimized subqueries).

Historically, we've used a proprietary, pre-compiled C++ tool located at `/app/plan_validator` to classify these PostgreSQL query plans. However, this legacy binary is incredibly slow, frequently bottlenecks our CI/CD pipeline, and the original source code has been lost. It is a stripped binary.

Your task is to write a fast, drop-in replacement in Go.
You must create a Go program at `/home/user/fast_validator.go` that takes a single file path as a command-line argument. The program should parse the PostgreSQL EXPLAIN JSON plan and output exactly `VALID` or `INVALID` to standard output.

To help you deduce the validation rules, we have provided two directories of query plans:
- `/home/user/corpus/clean/` : Contains 50 query plans that the legacy validator considers safe.
- `/home/user/corpus/evil/` : Contains 50 query plans that the legacy validator rejects due to specific inefficient join or subquery patterns.

You can use `/app/plan_validator <file>` as an oracle to test your hypotheses, or you can analyze the binary directly using standard reverse-engineering tools (`objdump`, `strings`, `strace`, etc. are available). 

Requirements for your Go program:
1. Must be written to `/home/user/fast_validator.go`.
2. Must accept a file path as `os.Args[1]`.
3. Must print ONLY `VALID` or `INVALID` to stdout (followed by a newline).
4. Must perfectly separate the `clean` and `evil` corpora, and also correctly classify a hidden evaluation set of plans using the exact same rules as the legacy binary.

Build the program (`go build fast_validator.go`) and ensure it works flawlessly against the provided corpora before considering the task complete.