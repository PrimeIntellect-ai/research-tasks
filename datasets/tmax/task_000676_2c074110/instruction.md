You are tasked with porting a legacy mathematical checksum virtual machine to run in a minimal Linux container.

The system consists of a core C library that handles CRC calculations, and a Python wrapper that acts as the VM emulator. However, the system is currently broken:
1. The C library (`/app/crc.c`) contains Undefined Behavior (an array out-of-bounds error and memory mismanagement) that causes it to crash or produce garbage. 
2. The exact mathematical parameters for the VM (the CRC polynomial, the initial CRC value, and the instruction set mappings) were lost from the source code, but a screenshot of the original specification document is available at `/app/spec.png`.
3. The Python emulator needs to be written from scratch to link with the fixed C library and execute the VM bytecode.

Your tasks are:
1. Extract the VM specifications from `/app/spec.png`. You can use the preinstalled `tesseract` OCR tool.
2. Fix the C code in `/app/crc.c` so that it is memory safe and logically correct. Compile it into a shared library named `/app/libcrc.so` using `gcc`.
3. Write a Python script `/app/run.py` that implements the VM emulator.

**VM Execution Rules:**
- The VM maintains an 8-bit accumulator `A` (starts at `0x00`) and a 16-bit `CRC` (starts at the INIT value from the image).
- The input to `/app/run.py` will be a single command-line argument containing an even-length hex string (e.g., `0105020A`).
- The hex string is processed in pairs of bytes: `[opcode, value]`.
- For each pair:
  a. Update `A` by performing the operation specified by the `opcode` (from the image) using `value` as the operand. All operations on `A` wrap around to fit in 8 bits (modulo 256).
  b. Update the `CRC` by passing the *current* `CRC`, the *new* value of `A`, and the `POLY` (from the image) to the `compute_crc` function in your compiled `libcrc.so` via Python's `ctypes`.
- After processing all pairs, your Python script must print the final 16-bit CRC as an uppercase 4-character hex string (e.g., `04A3`). Do not print anything else.

**C Library Signature:**
The function in `/app/crc.c` has the signature:
`uint16_t compute_crc(uint16_t current_crc, uint8_t data, uint16_t poly);`
It processes the 8 bits of `data` (MSB first) into the `current_crc`.

Ensure your Python script is executable and prints only the final 4-character hex result to stdout.