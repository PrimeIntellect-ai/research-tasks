You are an engineer setting up the first stage of a polyglot data pipeline. The pipeline uses Go to generate mathematically intensive data, serializes it, and then relies on shell utilities (`jq`) to extract configurations for downstream C++ workers. 

Your task is to implement the Go generator and the build system (`Makefile`) that glues the steps together.

Step 1: Create a Go program at `/home/user/generator.go`
- Define a custom data structure (e.g., a struct) to hold information about a number in the Fibonacci sequence. It must contain the fields: `n` (the index, starting at 0), `fib` (the Fibonacci number at index `n`), and `lpf` (the Largest Prime Factor of that Fibonacci number).
- Implement a numerical algorithm to generate the first 40 Fibonacci numbers (from N=0 to N=39). 
  - Note: F(0) = 0, F(1) = 1, F(2) = 1, etc.
- Implement an algorithm to find the Largest Prime Factor (LPF) for each of these Fibonacci numbers. 
  - For `fib` values of 0 and 1, set the `lpf` to 0.
- Serialize the sequence (an array of your custom structs) into a JSON array of objects.
- Write the serialized JSON output to `/home/user/data.json`.
  - The JSON objects must precisely use the keys: `"n"`, `"fib"`, and `"lpf"`.

Step 2: Create the polyglot build system at `/home/user/Makefile`
Write a Makefile with the following targets:
- `build`: Compiles `/home/user/generator.go` into an executable named `generator` in the same directory.
- `run`: Executes the `generator` binary to produce `/home/user/data.json`.
- `extract`: Uses the shell utility `jq` to parse `/home/user/data.json`, extract the `lpf` value of the 20th index (i.e., where `n` = 20), and saves ONLY that integer value to `/home/user/answer.txt`.
- `all`: A default target that sequentially runs `build`, `run`, and `extract`.

Step 3: Execution
Run `make all` in the `/home/user` directory to execute your pipeline and produce the final `/home/user/answer.txt` file. Make sure all files are located exactly where specified.