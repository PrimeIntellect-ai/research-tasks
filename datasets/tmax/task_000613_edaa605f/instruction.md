You are an engineer working on migrating legacy tools to run in a minimal, Alpine-based container environment. We have a legacy tool, an ELF executable located at `/app/version_evaluator`, which evaluates complex semantic version constraint expressions. Unfortunately, it is a stripped binary dynamically linked against an older glibc, which prevents it from running natively in our new minimal containers.

Your task is to reverse-engineer the behavior of this black-box binary and perfectly port its functionality into a standalone Python script.

The binary is invoked from the command line as follows:
`/app/version_evaluator "<constraint_expression>" "<target_version>"`

Examples of constraint expressions:
- `>=1.2.3 && <2.0.0`
- `(>2.1.0 || ==2.0.0-rc.1) && !=2.1.5`

The target version is a standard semantic version string (e.g., `1.5.0` or `2.0.0-alpha.2`).

The binary outputs exactly one of the following strings to standard output, followed by a newline:
- `MATCH` (if the target version satisfies the constraint)
- `NO_MATCH` (if the target version does not satisfy the constraint)
- `INVALID` (if either the constraint expression or the target version violates standard semantic versioning rules or has syntax errors).

Exit codes:
- `0` for `MATCH` and `NO_MATCH`
- `1` for `INVALID`

Create your ported tool at `/home/user/evaluator.py`. It must accept exactly the same two positional arguments and produce bit-exact equivalent standard output and exit codes as the original binary for any valid or invalid input.