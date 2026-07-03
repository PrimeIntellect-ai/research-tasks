You are a network engineer troubleshooting an automated connectivity logging system.

Part 1: The Misconfigured Git Hook
There is a local bare Git repository at `/home/user/netconfig.git`. Whenever network configurations are pushed to it, a `post-receive` hook runs a connectivity check. However, the hook is currently writing its output to the wrong location or failing entirely because the environment variables (specifically `LOG_DIR`) available during the hook execution differ from a standard interactive shell.
We received an automated voice alert about this failure. Please transcribe the audio file located at `/app/alert.wav` (you can use `whisper` or write a quick Python script using `import whisper`). The audio message will tell you the correct absolute path that `LOG_DIR` must be set to.
Once you have the path:
1. Create the directory mentioned in the audio.
2. Modify `/home/user/netconfig.git/hooks/post-receive` so that it exports the correct `LOG_DIR` before running its payload. Make sure the hook is executable.

Part 2: The Log Normalizer (C++)
The connectivity check generates raw IP status logs. You need to write a robust C++ filter program that standardizes these logs. 
Create your source file at `/home/user/ip_normalizer.cpp` and compile it to `/home/user/ip_normalizer`.

Your C++ program must read exactly one line from Standard Input (stdin) without a trailing newline, and output exactly one line to Standard Output (stdout), followed by a newline `\n`.
The rules are strictly:
1. If the input matches the exact format `A.B.C.D STATUS` where A, B, C, and D are integers between 0 and 255 (inclusive) with no leading zeros (unless the value is exactly "0"), and STATUS is either exactly `UP` or `DOWN`.
2. If the input is valid, the output must be: `[AAA.BBB.CCC.DDD] STATUS` where each octet is strictly zero-padded to 3 digits. (e.g., `192.168.1.0 UP` becomes `[192.168.001.000] UP`).
3. If the input does not perfectly match these rules (e.g., extra spaces, out of range octets, invalid status, extra characters), the program must output exactly `INVALID`.

Your compiled program `/home/user/ip_normalizer` will be heavily fuzzed against a reference binary `/app/oracle_normalizer` to ensure bit-exact output equivalence for tens of thousands of random and targeted inputs.