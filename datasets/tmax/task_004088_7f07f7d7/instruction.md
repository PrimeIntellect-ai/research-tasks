You are an integration developer building a testing framework for internal APIs. As part of this, you need to implement a lightweight Bash-based interpreter for a custom API testing Domain Specific Language (DSL). You also need to fix and compile a vendored C library used by the interpreter for string manipulation.

### Part 1: Fix the Vendored Package
We rely on a custom string manipulation utility located at `/app/string_utils-1.2.0`. 
However, the package's `Makefile` is broken due to a recent environment migration. It fails to build because it hardcodes a missing compiler and forgets to link the math library.
1. Fix the `Makefile` in `/app/string_utils-1.2.0` so that it successfully compiles using `gcc` and correctly links with `-lm`.
2. Run `make` to produce the executable `/app/string_utils-1.2.0/str_tool`. This tool supports an `encode` command that URL-encodes a given string.

### Part 2: Implement the DSL Interpreter
Write a Bash script at `/home/user/api_interpreter.sh` that takes exactly one argument: a string containing a program in our custom DSL.
The DSL consists of commands separated by the pipe character `|`. Your script must evaluate the commands in order and maintain a state of variables.

**DSL Commands:**
- `SET <var> <value>`: Sets the variable `<var>` to the string `<value>`. If `<value>` has spaces, it will be quoted in the input.
- `APPEND <var> <value>`: Appends `<value>` to `<var>`, separated by a comma. If `<var>` does not exist, treat it as `SET <var> <value>`.
- `SORT <var>`: Treats the string in `<var>` as a comma-separated list of items, sorts them alphabetically, and updates `<var>` with the sorted comma-separated string.
- `MERGE <var1> <var2>`: Takes the comma-separated lists from `<var1>` and `<var2>`, combines them, removes any duplicates, sorts them alphabetically, and stores the result in `<var1>`.
- `URLENCODE <var>`: Calls the fixed `/app/string_utils-1.2.0/str_tool encode` on the value of `<var>` and updates `<var>` with the output.
- `JSON`: Serializes all currently defined variables into a single valid JSON object, where keys are sorted alphabetically, and prints it to `stdout`. Execution terminates after a `JSON` command.

**Example Input:**
`/home/user/api_interpreter.sh "SET endpoints /users,/auth | APPEND endpoints /admin | SORT endpoints | URLENCODE endpoints | SET method POST | JSON"`

**Expected Output:**
```json
{
  "endpoints": "%2Fadmin%2C%2Fauth%2C%2Fusers",
  "method": "POST"
}
```

**Requirements:**
- Ensure `/home/user/api_interpreter.sh` is executable.
- The script must be written in Bash.
- Only standard Linux utilities (e.g., `jq`, `sort`, `awk`, `sed`) and the compiled `str_tool` may be used.
- Your interpreter must perfectly match the expected state mechanics and output bit-exact JSON. An automated fuzzer will test your script against thousands of random DSL programs.