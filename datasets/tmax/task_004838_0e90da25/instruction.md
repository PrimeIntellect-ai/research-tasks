You are an integration developer responsible for testing APIs and maintaining our CI/CD pipelines. We recently experienced a catastrophic data loss event and lost the source code for our schema migration and versioning tool, which was written in Go. All we have left is the compiled, stripped binary located at `/app/schema_migrator`.

Your task is to reverse-engineer the behavior of this binary through black-box testing and write a bit-exact equivalent Python script at `/home/user/migrator_rebuilt.py`.

The `/app/schema_migrator` binary reads strings from standard input (line by line) until EOF, and prints exactly one response line to standard output for each input line. It evaluates semantic versions and schema migration transition requests.

You must:
1. Orchestrate your own tests against `/app/schema_migrator` to deduce its parsing rules, semantic version comparison logic, state changes, and string output formats.
2. Setup a local iterative testing loop to refine your Python script against the binary.
3. Write the final implementation in `/home/user/migrator_rebuilt.py`. 
4. The script must read from standard input line-by-line (stripping the trailing newline) and print the appropriate response.

Your Python script will be verified using a fuzzing framework that compares its standard output to the `/app/schema_migrator` oracle across tens of thousands of randomly generated test cases. Even a single character difference or a trailing space mismatch will cause the verification to fail. 

Use standard Python 3. The `semver` or `packaging` libraries are NOT required; the binary uses its own strict integer-based triplet logic (`X.Y.Z`) with some specific migration transition rules.