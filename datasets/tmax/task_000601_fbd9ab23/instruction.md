I need to organize a massive archive of project crash logs, but I'm running into a tooling issue. A former developer built a custom CLI tool to compress these multi-line logs using a proprietary differential compression algorithm, but they only left behind a stripped binary located at `/app/log_packer`. We lost the original source code.

Your task is to completely reverse-engineer the behavior of this binary and reimplement it perfectly in Rust. 

Here is what I know about the tool and the log formats:
1. **Multi-line log parsing:** The tool takes a stream of concatenated log records via standard input (`stdin`) and writes the compressed binary format to standard output (`stdout`). 
2. **Standard stream usage:** You can test the binary by echoing or cat-ing data into `/app/log_packer` and inspecting the hex-dumped output.
3. **Record Separation:** Each individual log record in the input text stream is terminated by the exact string `===\n`. A log record can contain multiple lines of text (like stack traces) before this terminator.
4. **Differential Compression:** The tool supposedly compares consecutive multi-line log records to save space, outputting some combination of common prefix lengths and the varying suffixes.
5. **Output Format:** The output is a custom binary format.

What you must do:
1. Use bash standard stream redirection (`<`, `>`, `|`), `xxd`, `echo`, and other coreutils to perform black-box testing against `/app/log_packer`. Feed it various test strings to deduce its exact binary output format and differential compression algorithm.
2. Initialize a new Rust project at `/home/user/log_packer`.
3. Write a Rust program (`src/main.rs`) that exactly replicates the behavior of `/app/log_packer`. It must read from `stdin`, process the records exactly the same way, and write the exact same binary format to `stdout`.
4. Compile your project in release mode so the final executable is located at `/home/user/log_packer/target/release/log_packer`.

An automated test will generate thousands of random multi-line log sequences, feed them through both your Rust binary and the original `/app/log_packer`, and assert that the byte-for-byte outputs are strictly identical.