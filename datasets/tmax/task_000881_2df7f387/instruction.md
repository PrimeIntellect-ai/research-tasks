You are acting as a penetration tester and security engineer. We have a legacy backend service running a proprietary protocol, but the source code has been lost. The stripped binary is available at `/app/legacy_processor`. 

Through preliminary service auditing, we suspect this binary has a command injection vulnerability (CWE-78) when parsing input. It accepts multiline text requests on standard input. 

Your objectives are:
1. Analyze the stripped binary `/app/legacy_processor` to understand its input structure and identify the exact characters and patterns that trigger the command injection vulnerability. You may use standard tools like `strings`, `objdump`, or `gdb` to reverse-engineer it, or treat it as a black-box oracle and fuzz it.
2. Develop a strict C++ input validation filter that classifies requests as either benign ("clean") or malicious ("evil"). 
3. Write your filter in C++ at `/home/user/filter.cpp` and compile it to `/home/user/filter`.

The filter `/home/user/filter` must:
- Read the entire request from standard input (`stdin`).
- Exit with status code `0` if the input is safe (clean).
- Exit with status code `1` if the input contains malicious shell injection characters or violates the expected protocol structure.

To assist you, there are a few sample inputs in `/app/samples/`. However, the final verification will test your filter against a hidden adversarial corpus of malicious inputs and a hidden corpus of legitimate clean inputs.

Your solution must be robust: it must catch 100% of the hidden malicious inputs without blocking any of the clean inputs. Compile your code with `g++ -O2 -o /home/user/filter /home/user/filter.cpp`.