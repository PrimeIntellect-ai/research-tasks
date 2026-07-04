You are an incident responder analyzing a compromised Linux server. You have identified a custom authentication mechanism used by the attackers, implemented as a shared library (`libtoken.so`). Network logs indicate they have successfully authenticated using a challenge-response token system.

Your goal is to determine the attacker's secret 4-character PIN (consisting only of lowercase english letters, `a-z`) and save it to a file.

Here is what you have in `/home/user/evidence/`:
1. `auth.log`: A log file containing challenge-response pairs. You must identify the single successful authentication event to get the target Challenge and Token.
2. `libtoken.so`: An ELF shared object used for token generation. It exports a C function with the following signature:
   `uint32_t generate_token(const char* pin, uint32_t challenge);`

Perform the following tasks:
1. Parse `/home/user/evidence/auth.log` to find the successful authentication event, extracting the `Challenge` (decimal integer) and the `Token` (hexadecimal integer).
2. Write a Python script to brute-force the 4-character lowercase PIN. Your script must load and use the `generate_token` function from `/home/user/evidence/libtoken.so` via the `ctypes` module.
3. Once you find the PIN that generates the successful Token for the given Challenge, write the exact 4-character PIN string to a file named `/home/user/cracked_pin.txt`. Do not include any newlines or extra text in this file.

*Note: The PIN is exactly 4 lowercase alphabetical characters. Standard brute-force (26^4 = 456,976 combinations) will complete in seconds.*