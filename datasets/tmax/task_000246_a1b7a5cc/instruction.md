I need you to develop a small virtual machine utility in C that evaluates mathematical expressions encoded in a custom bytecode. The specification for this bytecode, including the hexadecimal opcode mappings and a required modulo constant for all operations, was unfortunately only saved as a screenshot at `/app/spec.png`.

Here is your workflow:
1. Extract the text from the image at `/app/spec.png` (using `tesseract` or similar tools). The image contains mappings for `OP_PUSH`, `OP_ADD`, `OP_SUB`, `OP_MUL`, `OP_POP`, and a `CONST_MOD` value.
2. Implement an interpreter in C (`/home/user/math_vm.c`). The virtual machine should:
   - Use a simple integer stack (max depth 1024).
   - Read a sequence of bytes from `stdin` until EOF.
   - For `OP_PUSH`, read the next 4 bytes as a 32-bit signed integer (little-endian) and push it onto the stack.
   - For arithmetic operations, pop the top two values, apply the operation (e.g., `top_val_2 + top_val_1`), apply modulo `CONST_MOD` (ensure positive result), and push the result back.
   - For `OP_POP`, remove the top item.
   - Ignore unrecognized bytes.
   - At EOF, print the integer value at the top of the stack to `stdout` (followed by a newline). If the stack is empty, print `0`.
3. Compile your code to `/home/user/math_vm`.
4. Ensure your implementation's behavior exactly matches our reference implementation located at `/app/oracle_vm` for any sequence of bytes.

Make sure your C program handles edge cases like stack underflow gracefully (e.g., push 0 or ignore the operation, deduce from the oracle if necessary, but assume standard ignore-if-underflow logic).