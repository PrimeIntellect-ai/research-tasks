You are a platform engineer maintaining a lightweight CI/CD pipeline system. You need to implement a custom pipeline runner in C that parses a simple pipeline definition language, evaluates system constraints, and executes build commands if constraints are met.

Your task has three parts:
1. Write the pipeline interpreter in C (`/home/user/runner.c`).
2. Create a `Makefile` to compile it (`/home/user/Makefile`).
3. Run the compiled tool against a provided pipeline file and generate a log.

**1. The Pipeline Interpreter**
Write a C program `/home/user/runner.c` that takes exactly one command-line argument: the path to a pipeline file.
The pipeline file has the following format. Each line is either a constraint or a command:
- `REQUIRE <ENV_VAR> <OP> <VALUE>`
- `EXEC <command...>`

**Rules for evaluation:**
- The interpreter maintains an internal boolean state called `can_execute`, initially set to `1` (true).
- When it reads a `REQUIRE` line, it reads the environment variable `<ENV_VAR>`. If the environment variable is not set, treat its value as `0`.
- It parses `<VALUE>` as an integer.
- `<OP>` can be `==`, `>`, or `<`.
- It evaluates the integer comparison: `(value of ENV_VAR) OP (VALUE)`. If the condition is true, `can_execute = 1`. If false, `can_execute = 0`.
- When it reads an `EXEC` line, if `can_execute == 1`, it executes the remainder of the line (the command string) using the C `system()` function. If `can_execute == 0`, it skips the command.
- Empty lines or lines that do not start with `REQUIRE` or `EXEC` should be ignored.
- Lines will not exceed 256 characters. `<ENV_VAR>` will not exceed 64 characters.

**2. The Build System**
Create a `/home/user/Makefile` with the following requirements:
- The default target (`all`) should compile `runner.c` into an executable named `ci_runner`.
- Use `gcc` with the flags `-Wall -Wextra -O2`.
- Include a `clean` target that removes `ci_runner`.

**3. Execution & Verification**
We have placed a test pipeline file at `/home/user/pipeline.txt`.
Set the following environment variables in your shell, build your program, and run it:
```bash
export OS_LINUX=1
export MEM_GB=16
export ARCH_X86=0
make
./ci_runner /home/user/pipeline.txt
```

Your program should execute the valid steps in `/home/user/pipeline.txt`, which will append output to `/home/user/execution.log`.
Do not manually edit `/home/user/pipeline.txt` or `/home/user/execution.log`.