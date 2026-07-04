You are an integration developer tasked with modernizing our API backend components. We have a legacy data-processing binary located at `/app/legacy_calc` which evaluates mathematical expressions sent as JSON payloads. This binary is a stripped, unmaintained executable, and we need to replace it with a robust Go implementation.

Your task:
1. Reverse-engineer the behavior of the `/app/legacy_calc` binary. It reads a JSON payload from `stdin` and writes a JSON response to `stdout`.
2. Discover its syntax rules, operator precedence (watch out for quirks!), error handling, and exact JSON formatting. 
3. Write a Go program at `/home/user/calc.go` that perfectly replicates the behavior of the legacy binary.
4. Compile your Go code to an executable at `/home/user/calc`.

The input JSON generally looks like:
`{"expression": "a + 2 * b", "context": {"a": 5, "b": 3}}`

The output JSON will indicate success and the integer result, or an error and the reason. You must match the legacy binary's output exactly (including whitespace and key ordering, if predictable, or rely on standard JSON marshalling if it matches).

You should test your implementation thoroughly against the legacy binary. We will verify your solution by generating thousands of random valid and invalid JSON inputs, feeding them to both `/app/legacy_calc` and your `/home/user/calc`, and ensuring the outputs are bit-for-bit identical.