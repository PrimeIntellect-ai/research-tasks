You are a web developer building a real-time collaborative animation canvas. Clients connect via WebSockets and send small "animation bytecodes" to be executed on the server. To protect the server from Denial of Service (DoS) attacks and data corruption, you need to write a strict validator for these bytecode payloads.

We have captured a video signal used to synchronize the daily cryptographic seed for the checksums. This video is located at `/app/sync_signal.mp4`. 
The video is exactly 10 seconds long, playing at 1 frame per second (10 frames total). Each frame is either completely black or completely white.
A black frame represents the bit `0`, and a white frame represents the bit `1`. Reading the frames chronologically from second 0 to second 9 gives a 10-bit binary number (most significant bit first). This integer is the `SEED`.

You have been provided with two directories containing sample payload files:
- `/app/corpus/clean/`: Contains perfectly valid payloads.
- `/app/corpus/evil/`: Contains malformed or malicious payloads that must be rejected.

Each payload file is a plain text file. 
The first line is always: `CHECKSUM: <integer>`
The remaining lines are the bytecode instructions, one per line.

Your task is to write a script at `/home/user/validator.sh` or `/home/user/validator.py` (your choice of language) that takes a single file path as a command-line argument and prints exactly `ACCEPT` or `REJECT` to standard output.

Validation Rules (a payload must pass ALL of these to be ACCEPTED):
1. **Checksum Verification**: The sum of the ASCII values of all characters in the instruction lines (including newline characters `\n`), plus the `SEED` extracted from the video, must exactly equal the `<integer>` provided in the `CHECKSUM` line.
2. **Emulator Safety**: You must implement a simple emulator to simulate the bytecode execution. The machine has a stack (maximum depth of 10 integers). The program starts at line 1 of the instructions.
    - `PUSH <int>`: Pushes an integer onto the stack. Fails if stack depth exceeds 10.
    - `POP`: Removes the top item from the stack. Fails if stack is empty.
    - `ADD`: Pops two items, adds them, pushes the result. Fails if < 2 items on stack.
    - `SUB`: Pops two items (A, then B), subtracts them (B - A), pushes the result. Fails if < 2 items.
    - `JMP <offset>`: Jumps the instruction pointer by `<offset>` lines (e.g., `JMP -2` goes back two lines). Fails if it jumps outside the bounds of the program.
    - `HALT`: Successfully terminates the execution.
3. **Execution Limits**: The program MUST reach a `HALT` instruction within 100 execution steps. If it executes 101 steps without halting, it is considered an infinite loop and must be REJECTED.

Write the script to analyze the payloads. You can use tools like `ffmpeg` to analyze the video. Your final deliverable should be the executable validator script at `/home/user/validator.py` (or whatever extension you choose, as long as it's executable and handles `<filepath>` as `$1`).