You are an engineer tasked with porting a plugin-loading system into a minimal Linux container. The minimal container lacks the original C++ toolchain and validation binaries, so you need to replicate the shared library ABI validation logic using a lightweight Python script.

In the old system, a C function parsed a custom rule file to determine if a shared library (`.so`) matched the required ABI (ELF class and specific exported dynamic symbols) before conditionally building the load plan. The old C snippet for the rule evaluation logic was:

```c
// legacy_validator.c (Snippet)
bool evaluate_rule(int elf_class, bool has_symbol, const char* op, const char* expected_class) {
    bool class_match = (elf_class == 32 && strcmp(expected_class, "ELF32") == 0) ||
                       (elf_class == 64 && strcmp(expected_class, "ELF64") == 0);
    
    if (strcmp(op, "AND") == 0) {
        return class_match && has_symbol;
    } else if (strcmp(op, "OR") == 0) {
        return class_match || has_symbol;
    }
    return false;
}
```

The rule file `/home/user/plugin_rules.txt` uses the format:
`<plugin_filename> : CLASS=<ELF32|ELF64> <AND|OR> SYM=<symbol_name>`

Example:
`libalpha.so : CLASS=ELF64 AND SYM=plugin_init`

Your task is to write a Python script `/home/user/validate_plugins.py` that:
1. Translates the above C logic into Python.
2. Acts as a parser and state machine to read `/home/user/plugin_rules.txt`.
3. Inspects the shared libraries located in `/home/user/plugins/` to extract their ELF class (32-bit or 64-bit) and checks if they export the specified dynamic symbol (you may use system tools like `readelf` via `subprocess`).
4. Evaluates the conditions for each plugin specified in the rules file.
5. Generates a load plan in JSON format at `/home/user/load_plan.json`. 

The JSON must be a simple dictionary mapping the plugin filename to a boolean indicating whether it passed the rule check. Example format for `/home/user/load_plan.json`:
```json
{
  "libalpha.so": true,
  "libbeta.so": false
}
```

Ensure your script handles standard ELF introspection properly and correctly evaluates the `AND`/`OR` expressions based on the library's actual architecture and exported ABI.