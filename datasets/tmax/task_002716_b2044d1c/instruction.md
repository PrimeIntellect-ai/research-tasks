You are a QA engineer setting up a test environment for a new mathematical data-streaming engine. The engine receives numerical sequences via WebSocket, sorts them, and calculates differential gaps.

Currently, the project is broken, and you need to fix it, reverse-engineer a proprietary filter, and integrate it. 

Your objectives are:

1. **Fix the Build (Circular Import):**
   The Go module located at `/home/user/qa-env/wsprocessor` fails to compile. The `sorter` package and the `differ` package have a circular import dependency. Refactor the code by extracting shared types or interfaces into a new package (e.g., `models` or `common`) so that `go build ./...` succeeds without changing the external behavior of the packages.

2. **Reverse Engineer the Mathematical Filter:**
   The company uses a proprietary algorithm to filter out "noisy" data sequences before processing. The source code is lost, but a stripped, compiled binary of the oracle is available at `/app/seq_oracle`. 
   The oracle reads a space-separated list of integers from standard input. It exits with code `0` if the sequence is valid ("clean"), and exits with code `1` if it is invalid ("evil").
   You must deduce the mathematical rule implemented by this binary. Use standard CLI tools or write your own Go scripts to test inputs against it. (Hint: The rule involves sorting, merging, and diffing adjacent elements).

3. **Implement the Filter & Classifier:**
   Inside the project, create a new package `filter` with a file `filter.go` containing:
   `func Classify(seq []int) bool`
   It should return `true` for clean sequences and `false` for evil sequences, matching the behavior of `/app/seq_oracle`.
   
   Then, update the main application to produce a CLI tool. When built, the binary should be placed at `/home/user/qa-env/wsprocessor/bin/classifier`. 
   The CLI must accept a file path as an argument. The file will contain space-separated integers. The CLI must print exactly `CLEAN` to standard output if the sequence is valid, and `EVIL` if it is invalid.

4. **WebSocket Mock Integration:**
   Update the WebSocket handler in `main.go` to use your new `filter.Classify` function. If a received JSON array of integers is classified as evil, the WebSocket server should respond with `{"status": "rejected"}`. If clean, it should respond with `{"status": "accepted"}`.

Verify your classifier CLI against the sample corpora located at:
- `/home/user/corpora/clean/` (all files here should evaluate to CLEAN)
- `/home/user/corpora/evil/` (all files here should evaluate to EVIL)