You are a build engineer managing a new artifact verification pipeline. The pipeline uses a custom bytecode language to define verification rules for build artifacts. 

Your task is to write a C program `/home/user/verifier.c` that parses and executes these bytecode rules. You must implement a stack-based emulator, a custom numerical algorithm, and a request rate-limiter.

The input file will be located at `/home/user/pipeline_jobs.txt`.
Each line follows the format: `JobID:HexString`
(e.g., `JobA:011005FF`)

**Virtual Machine Specification:**
- **Architecture:** Stack-based, maximum stack size of 16. Elements are 32-bit signed integers.
- **Execution:** Start at the first byte. Read opcodes and execute sequentially until a HALT, ERROR, or RATE_LIMIT condition occurs.
- **Standard Libraries:** You may use `<stdio.h>`, `<stdlib.h>`, `<string.h>`, `<stdint.h>`. You **MAY NOT** use `<math.h>`.

**Opcodes:**
- `0x01` (PUSH): The next byte is an 8-bit **signed** integer. Push it onto the stack.
- `0x02` (ADD): Pop A (top), Pop B. Push (B + A).
- `0x03` (SUB): Pop A (top), Pop B. Push (B - A).
- `0x04` (MUL): Pop A (top), Pop B. Push (B * A).
- `0x05` (ISQRT): Pop A. Compute the integer square root of A ($\lfloor\sqrt{A}\rfloor$). You must implement this using a numerical algorithm (like Newton's method or binary search) since `<math.h>` is banned. Push the result. If A < 0, halt execution immediately with an `ERROR` state.
- `0x06` (CHECK_API): Pop A. This simulates hitting an external validation API. 
  - **Rate Limiting:** A single job may only execute the `CHECK_API` instruction a maximum of 3 times. If a job attempts to execute a 4th `CHECK_API`, halt execution immediately with a `RATE_LIMIT` state.
  - If within limits: If A > 0, push `1`. If A <= 0, push `0`.
- `0xFF` (HALT): Halt execution successfully.

**Error Conditions:**
- If the stack underflows (popping when empty) or overflows (pushing when at 16 elements), halt with `ERROR`.
- If an unknown opcode is encountered, halt with `ERROR`.

**Output Specification:**
Your program should output the result of each job to a log file at `/home/user/verification_out.txt`.
For each job, write a single line: `JobID: RESULT`
- If it halted successfully, `RESULT` is the integer value at the top of the stack. (If the stack is empty, the result is `0`).
- If it encountered an error or invalid state, `RESULT` is `ERROR`.
- If it exceeded the API quota, `RESULT` is `RATE_LIMIT`.

Compile your C program into an executable named `/home/user/verifier` and run it against the input file.