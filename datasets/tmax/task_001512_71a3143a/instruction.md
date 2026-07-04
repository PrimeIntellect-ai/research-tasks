You are an operations engineer triaging an incident with our legacy telemetry pipeline. We have a stripped, legacy compiled binary located at `/app/bin/sensor_oracle` that processes raw sensor data. 

Recently, the hardware team reported that we need to migrate away from this binary. A previous engineer attempted to rewrite the processor in a modern scripting language and stored the WIP attempt in a local Git repository at `/app/legacy-port`. Unfortunately, that engineer left abruptly. The port currently fails to build/run, and preliminary tests showed that even when it did run, the output suffered from "precision loss" drift compared to the original binary's output.

Your objective is to create a fully functioning replacement script located at `/home/user/solution.sh`. This script (and any helper code it calls) must be a drop-in replacement that is **bit-exact equivalent** to `/app/bin/sensor_oracle`.

Here is what you need to know:
1. **I/O Format**: The `/app/bin/sensor_oracle` program reads from `stdin`. It expects a sequence of 8-character hexadecimal strings, one per line. Each hex string represents an IEEE-754 32-bit floating-point number. It outputs processed 8-character hex strings to `stdout`, one per line.
2. **The Logic**: The math formula is hidden. You will need to dig into the git repository at `/app/legacy-port` to find clues about the algorithm. 
3. **The Constants**: The old repo mentions some configuration constants, but they were lost. Fortunately, we have a core memory dump from a time the legacy binary crashed at `/app/dump/core.oracle`. You will need to analyze this dump to extract the exact constants used by the program.
4. **Precision Loss**: The most critical part of this task is ensuring there is zero precision drift. The legacy binary performs its internal calculations using strict 32-bit single-precision floating-point arithmetic. Standard 64-bit float math (like default Python floats) will produce slightly different rounding results, which will fail our automated checks.

**Requirements**:
- Produce a script at `/home/user/solution.sh` that accepts data via stdin and prints to stdout in the exact same format as `/app/bin/sensor_oracle`.
- You can use any programming language you prefer (Python, C, Node, etc.) as long as it is invoked correctly by `/home/user/solution.sh`.
- Do not hardcode a limited set of answers. An automated fuzzing verifier will feed 1,000 random hex-encoded floats into both your solution and the legacy binary. The outputs must match perfectly.