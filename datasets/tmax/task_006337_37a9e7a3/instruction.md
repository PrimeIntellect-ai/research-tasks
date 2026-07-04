You are a support engineer investigating a customer escalation. The customer reported that our high-performance query evaluation engine crashes when processing their batch queries. 

The binary is located at `/home/user/math_evaluator`. It takes a single argument: the path to a CSV file containing query parameters.
The customer's input file is provided at `/home/user/queries.csv`.

Because this is a production binary, it has been stripped of debugging symbols. Your task is to collect diagnostics to pass onto the C++ development team.

You must perform the following steps:
1. **Test Minimization (Delta Debugging):** Isolate the exact single line in `/home/user/queries.csv` that triggers the crash.
2. **Crash Analysis:** Run the stripped binary with the minimized input using a debugger or dynamic analysis tool to identify the crash signal and the exact assembly instruction that causes the fault.

Once you have gathered the diagnostics, create a report at `/home/user/diagnostic_report.txt` exactly in the following format:

```text
FAILING_QUERY: <the exact comma-separated line that causes the crash>
CRASH_SIGNAL: <the signal that killed the process, e.g., SIGSEGV, SIGILL, SIGFPE>
CRASH_INSTRUCTION_MNEMONIC: <the assembly instruction mnemonic at the instruction pointer when it crashed, e.g., mov, idiv, add>
```

Example of the expected format:
```text
FAILING_QUERY: 12,34,56,78
CRASH_SIGNAL: SIGSEGV
CRASH_INSTRUCTION_MNEMONIC: mov
```

Make sure the file `/home/user/diagnostic_report.txt` is strictly formatted as above. Do not include any other text in the file.