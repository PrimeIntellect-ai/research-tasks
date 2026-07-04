You are an open-source maintainer reviewing a broken Pull Request for a project called `aud-eval`, a Go-based distributed math evaluation engine. The PR branch is already checked out at `/home/user/aud-eval`.

The goal of this tool is to process a large dataset of mathematical expressions, verify their integrity using a custom checksum, evaluate them via a custom Abstract Syntax Tree (AST), and do so concurrently to achieve high throughput. Furthermore, the evaluation rules depend on a parameter dictated in an audio transmission.

The PR author made a mess:
1. The Go code processes expressions sequentially, making it incredibly slow.
2. The expression parser (AST implementation) is incomplete and fails on nested parentheses.
3. The custom checksum validation is stubbed out.
4. The system parameter (modulus) is hardcoded incorrectly because the author didn't transcribe the audio instructions.

Your task is to fix the PR and finalize the system:
1. **Transcribe the Audio**: An audio file is located at `/app/transmission.wav`. Transcribe it using the pre-installed `whisper` CLI (or any method you prefer). The audio dictates a specific integer modulus value that must be applied to all final evaluation results.
2. **Fix the Parser**: Modify `parser.go` to correctly parse mathematical expressions (supporting `+`, `-`, `*`, `/`, and parentheses `()`) into a custom AST data structure, and evaluate them.
3. **Implement Checksum**: Each line in `equations.txt` is formatted as `<expression> | <checksum>`. The checksum is an error-correcting code defined as the sum of the ASCII values of the characters in the `<expression>` string (excluding spaces). Reject any line where the checksum does not match.
4. **Go Concurrency**: Refactor `main.go` to use goroutines and channels. The system must process the 500,000 lines in `equations.txt` concurrently.
5. **Output**: Write the valid, correctly evaluated results (after applying the modulo dictated by the audio) to `/home/user/aud-eval/results.csv`, one per line, formatted as `<expression>,<evaluated_result_modulo>`. 

A test script will measure the runtime and accuracy of your compiled Go binary. You must achieve a substantial speedup over the sequential baseline and 100% accuracy. Write your finalized code, compile it to `bin/aud-eval`, and leave it ready.