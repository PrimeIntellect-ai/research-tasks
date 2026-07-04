You are an operating systems programmer tasked with fixing a C/C++ build issue and performing a schema migration.

In `/home/user/project`, you have a tool called `evaluator.cpp` that is designed to evaluate postfix mathematical expressions. It relies on a pre-compiled legacy C library (`libexpr.so` and its header `expr.h`). 

Currently, compiling `evaluator.cpp` fails with a linking error: `undefined reference to evaluate_postfix`.

Your objectives:
1. **Fix the Linking Issue**: Modify `/home/user/project/evaluator.cpp` or `/home/user/project/expr.h` so that it successfully links against the C library without changing the core logic. 
2. **Compile the Tool**: Compile `evaluator.cpp` into an executable named `/home/user/project/evaluator`. Ensure it dynamically links to `libexpr.so` in the same directory.
3. **Migrate the Schema**: You have a legacy schema file `/home/user/project/v1_schema.txt`. Every line in this file contains a Base64-encoded string representing a postfix mathematical expression. 
   Using your compiled `evaluator` tool and standard bash utilities, decode each expression, evaluate it, and create a migrated schema file at `/home/user/project/v2_schema.json`.

The `v2_schema.json` file must be a strictly valid JSON array of objects, preserving the order of lines from the `v1_schema.txt`. Each object should have two keys:
- `"expression"`: the decoded string (e.g., `"3 4 +"`)
- `"value"`: the integer result returned by the `evaluator`

Example expected output format for `v2_schema.json`:
```json
[
  {
    "expression": "3 4 +",
    "value": 7
  }
]
```

Do not use external scripting languages like Python; use only bash, standard coreutils (like `base64`), `jq`, and your compiled C++ tool to generate the JSON.