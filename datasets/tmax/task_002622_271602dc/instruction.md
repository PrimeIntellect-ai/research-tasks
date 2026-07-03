We are currently running restore tests for our automated backup system. During a recent restore, several of our nginx services returned 502 Bad Gateway errors. After investigation, we realized this was due to upstream socket paths in the restored nginx configs being left in an obfuscated state. 

Our legacy backup system uses a proprietary, stripped binary located at `/app/path_decoder` to encode and decode filesystem and socket paths within configuration files. We are migrating away from this proprietary tool and need a native Python replacement.

Your task is to reverse-engineer the `/app/path_decoder` binary and write a functionally bit-exact equivalent Python script at `/home/user/solution.py`. 

Requirements:
- Your script must read input from standard input (`stdin`) until EOF.
- It must write the exact processed output to standard output (`stdout`).
- It must perfectly replicate the text transformation logic of the `/app/path_decoder` binary for any given input.
- You may use tools like `gdb`, `objdump`, `strings`, `ltrace`, or `strace` to analyze the binary, or treat it as a black box and deduce its behavior by passing it various test inputs.
- Make sure your script handles newlines and special characters exactly as the binary does.

An automated test suite will verify your solution by feeding hundreds of randomized strings to both the original binary and your Python script and asserting that the outputs are absolutely identical.