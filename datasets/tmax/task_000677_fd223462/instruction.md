You are a web developer tasked with building a new security feature: a Proof-of-Work (PoW) token validator for an API gateway. To prevent DDoS attacks, clients must solve a math puzzle presented in Reverse Polish Notation (RPN), compute its result, and provide a checksum of the puzzle string. 

You need to write a Rust command-line application that acts as an offline validator to process a batch of incoming requests concurrently. 

Here are the requirements:
1. Create a new Rust project called `pow-shield` in `/home/user/pow-shield`.
2. The application must read an input file containing batched requests. The file will be located at `/home/user/requests.txt`.
3. Each line in the input file represents a single request in the format: `RequestID|RPN_Expression|ExpectedResult|Checksum`.
    - `RequestID`: An alphanumeric string.
    - `RPN_Expression`: A mathematical expression in Reverse Polish Notation (space-separated). Supported operators are `+`, `-`, and `*`. Operands are 32-bit signed integers.
    - `ExpectedResult`: The claimed 32-bit integer result of the RPN expression.
    - `Checksum`: A simple integer checksum.
4. **Validation Rules**:
    - **Expression parsing & Numerical algorithm**: Evaluate the `RPN_Expression`. If it is invalid or does not exactly match the `ExpectedResult`, validation fails.
    - **Checksum**: Calculate the checksum of the `RPN_Expression` string. The checksum is the sum of the ASCII byte values of all characters in the exact `RPN_Expression` string (including spaces, but excluding the `|` delimiters or any newline characters), modulo 256. If it does not match the provided `Checksum`, validation fails.
5. **Concurrency**: Use Rust's `std::thread` and `mpsc` (Multi-Producer, Single-Consumer) channels to process the lines of the file concurrently. A main thread should read the file and dispatch work to a pool of at least 3 worker threads. The results should be sent back to a channel where the main thread writes them to the output file.
6. **Testing**: Write at least two unit tests in your Rust code (`#[test]`): one for the RPN evaluator and one for the checksum calculator.
7. Output the final validation results to `/home/user/results.log`. Each line must be formatted exactly as `RequestID: VALID` or `RequestID: INVALID`. The output order does not matter.
8. Run your tests and redirect the standard output and standard error of `cargo test` to `/home/user/test_results.log`.
9. Build the project using `cargo build --release` and run it against `/home/user/requests.txt`.

Ensure all files are created and placed in the exact paths specified.