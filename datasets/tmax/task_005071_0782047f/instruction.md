I am working on a multi-file Rust project that acts as a WebSocket backend. However, it currently fails to compile because it relies on a missing C executable that acts as a specialized state-machine parser for a legacy framing protocol.

I have a stripped binary of the legacy C parser located at `/app/ws_oracle`. 
Your task is to reverse-engineer the behavior of `/app/ws_oracle` and write a functionally identical C program. 

What we know about the oracle:
1. It reads binary data from `stdin` and writes parsed text to `stdout`.
2. It implements a simplified WebSocket-like state machine parser.
3. It handles basic framing (FIN bit, Opcodes, Payload length, Masking).
4. Unmasked and masked payloads are processed and output according to the state machine's internal rules.
5. If it encounters a Close frame or invalid data, it prints a specific sequence and terminates.

Your tasks:
1. Analyze `/app/ws_oracle` by feeding it various hex/binary inputs to deduce the exact framing format, state transitions, and output format.
2. Write the C implementation in `/home/user/src/parser.c`.
3. Compile your C code to `/home/user/bin/parser`. Note that the Rust project's build script is hardcoded to look for this exact executable path. Ensure it compiles cleanly with standard GCC.
4. Your compiled `/home/user/bin/parser` must exhibit bit-exact equivalent behavior to `/app/ws_oracle` for ANY arbitrary standard input sequence.

Please create the directory structure, write the C code, and compile the final binary. The testing framework will feed thousands of randomized byte sequences into both your binary and the oracle to verify identical output.