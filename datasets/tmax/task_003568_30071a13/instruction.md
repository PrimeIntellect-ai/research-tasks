You are a network security engineer investigating a recent breach. We suspect an attacker exploited a command injection vulnerability by bypassing JWT authentication and appending a rogue SSH public key to the server.

You have been provided with:
1. `/home/user/traffic.log`: A log file containing intercepted HTTP requests. The attacker injected their payload in the `cmd` field of a forged JWT token sent in the `Authorization: Bearer <token>` header.
2. `/home/user/decode.cpp`: A custom C++ utility written to extract and decode the payload section (the second part) of the JWTs from the log file.

However, `decode.cpp` is currently failing to decode the attacker's JWT because the developer used a standard Base64 decoding function, but JWTs use **Base64URL** encoding (where `+` is replaced by `-`, `/` is replaced by `_`, and padding `=` is often omitted).

Your task:
1. Fix `/home/user/decode.cpp` so that it correctly handles Base64URL decoding (convert `-` to `+`, `_` to `/`, and append `=` padding if necessary so the string length is a multiple of 4) before passing it to the existing `base64_decode` function.
2. Compile the fixed program using `g++ /home/user/decode.cpp -o /home/user/decode`.
3. Run the program to parse `/home/user/traffic.log`.
4. Inspect the decoded JWT payloads to find the forged token (where the user role is "admin" or the algorithm is "none") that contains a command injection payload attempting to write an SSH public key.
5. Extract **only** the injected SSH public key (starting with `ssh-rsa ` and ending with the comment/key data, without any surrounding quotes, echo commands, or backslashes) and save it exactly to `/home/user/rogue.pub`.