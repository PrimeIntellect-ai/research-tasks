You are a support engineer tasked with recovering the logic of a legacy data obfuscation tool that recently started crashing in production. The original source code has been lost.

We need you to reimplement the tool's core logic as a standalone Python script so we can replace the legacy binary entirely. 

Here is what we know and the diagnostic assets you have available:

1. **The Broken Binary:** 
   A copy of the legacy tool is located at `/app/legacy_tool.bin`. It takes a single string argument and outputs a hex-encoded obfuscated string. However, due to a memory corruption bug, it immediately segmentation faults if the input string is longer than 10 characters.
   
2. **The Crash Dump:**
   We captured a raw memory dump of the process right before a crash, saved at `/app/crash.dmp`. We know the obfuscation algorithm uses a hardcoded secret key string, which should be present in this memory dump. Look for a string located near the signature `XOR_KEY_SIG:`.

3. **The Architecture Notes:**
   We found an old whiteboard picture saved at `/app/whiteboard.png`. It contains the original developer's handwritten notes about the mathematical operations applied after the XOR step. You will need to extract the logic and offset constants from this image.

**Your Objective:**
Reverse-engineer the obfuscation algorithm using the broken binary (for short inputs), the crash dump, and the whiteboard image. 

Write a completely standalone Python script at `/home/user/clean_tool.py` that reimplements this logic perfectly.
- Your script must accept exactly one positional argument (the plaintext string).
- It must print only the final obfuscated hex string to standard output.
- It must not invoke the legacy binary (as the legacy binary crashes on inputs > 10 chars, and your script will be tested against much longer strings).
- It must handle any printable ASCII input.

Ensure your Python script is executable and functions identically to how the legacy binary *would* have functioned for inputs of any length.