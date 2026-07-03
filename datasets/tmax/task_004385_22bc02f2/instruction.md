You are an engineer tasked with porting a legacy evaluation tool to a minimal container environment. The legacy tool, `legacy_calc`, is written in C, dynamically linked against libraries not present in our new minimal container base, and needs to be rewritten purely in Go.

The legacy tool evaluates basic mathematical expressions and computes a custom integrity checksum on the result. It is located at `/app/bin/legacy_calc`.

**Your objective:**
1. **Analyze the legacy tool:** `/app/bin/legacy_calc` takes a single command-line argument containing a mathematical expression (e.g., `"3 + 5 * (10 - 2)"`). It evaluates it using standard integer arithmetic (supporting `+`, `-`, `*`, `/`, and `()`) and outputs a string in the exact format: `Result: <eval_result>, Checksum: <checksum_value>`.
2. **Extract missing parameters:** We lost the original source code. The custom checksum algorithm multiplies the absolute value of the evaluation result by a specific `MULTIPLIER` and then takes the result modulo a `MODULUS`. These specific constants are documented in a system architecture screenshot located at `/app/spec.png`. You will need to extract these constants from the image.
3. **Reimplement in Go:** Write a Go program at `/app/src/calc.go` that parses and evaluates the mathematical expressions, computes the checksum using the constants recovered from the image, and matches the legacy output exactly. Build the executable to `/app/bin/go_calc`.
4. **CI/CD Orchestration:** Create a test script at `/app/ci/test.sh` that compiles your Go code and tests it against the legacy tool with at least 5 different expressions to ensure parity. The script should exit with code 0 if all tests pass.

**Constraints & Details:**
- Your Go program must be compiled to `/app/bin/go_calc`.
- Standard operator precedence applies: `()` > `*`, `/` > `+`, `-`. All division is standard integer division (truncating towards zero). 
- The checksum is calculated as: `(abs(Result) * MULTIPLIER) % MODULUS`.
- The verifier will run a strict fuzzing tool that generates thousands of random valid mathematical expressions and feeds them to both `/app/bin/legacy_calc` and `/app/bin/go_calc`. The standard output of your Go binary must be bit-exact equivalent to the legacy oracle for every input.
- You may use any command line tools (like `tesseract`) to inspect the image.

Ensure your compiled binary is ready at `/app/bin/go_calc` before finishing.