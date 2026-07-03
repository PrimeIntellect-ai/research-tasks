You are a web developer working on a backend routing service. Our system handles legacy audio-routing requests using a custom bytecode language, but we are migrating away from the old compiled C++ binary (`/app/oracle_router`) to a native Python implementation.

Your task is to write a Python script at `/home/user/vm_router.py` that acts as an exact functional equivalent (emulator) to `/app/oracle_router`. 

Here is the context and specification:
1. The base payload data is derived from an audio file. We have a test audio file located at `/app/voicemail.wav`. 
2. You must transcribe this audio file. The transcription consists of a single English word. Convert this word to completely lowercase, with no whitespace or punctuation. This is your "Initial String".
3. Your script `/home/user/vm_router.py` must accept exactly one command-line argument: a hex-encoded string representing the routing opcodes (e.g., `0104410200`).
4. The script must parse the hex string into a stream of bytes, and execute the following virtual machine instructions sequentially on the "Initial String" until the stream ends or a HALT instruction is encountered.

**Bytecode Specification:**
*   `00` (HALT): Immediately stop execution and output the current state of the string.
*   `01` (UPPER): Convert the current string to uppercase.
*   `02` (REVERSE): Reverse the order of characters in the string.
*   `03 <byte>` (SLICE): The next byte is an integer `N`. Keep only the characters from index `N` to the end of the string. (If `N` >= length of string, the string becomes empty).
*   `04 <byte>` (APPEND): The next byte represents an ASCII character code. Append this character to the end of the string.
*   `05` (LOWER): Convert the current string to lowercase.

**Execution Rules:**
*   Any unrecognized opcode should be ignored (skip 1 byte).
*   If an opcode requiring an argument (like `03` or `04`) is the last byte in the stream, ignore the opcode and finish.
*   After the script finishes processing (or hits HALT), it must print the final mutated string to `stdout` (with no extra logging or newlines other than the standard print output).

To succeed, you must first figure out the hidden word in `/app/voicemail.wav` (you can install and use tools like `ffmpeg`, `whisper`, or `pocketsphinx` as needed). Then, implement the Python bytecode emulator. 

Your script will be aggressively fuzzed with thousands of random hex payloads and compared bit-for-bit against `/app/oracle_router`. Ensure all edge cases (empty strings, large slices) are handled gracefully and identically to the logic described. Make sure the script is executable or can be run via `python3 /home/user/vm_router.py <hex_string>`.