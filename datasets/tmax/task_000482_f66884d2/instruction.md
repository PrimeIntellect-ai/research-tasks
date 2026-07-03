You are a network security engineer investigating a proprietary authentication protocol used by legacy IoT devices on your network. You've intercepted some traffic and identified that the devices use a custom authentication token to establish sessions.

You are provided with a stripped, legacy authentication daemon extracted from one of the devices: `/app/legacy_token_validator`. 

You can test how it validates tokens by running it from the terminal. Its usage is:
`/app/legacy_token_validator <device_id_hex> <timestamp_int> <token_hex>`
It returns exit code 0 if the token is valid, and 1 if invalid.

Your objectives:
1. Reverse-engineer the token generation logic used by `/app/legacy_token_validator`.
2. Write a highly optimized C++ program located at `/home/user/fast_token_gen.cpp` that implements this token generation algorithm.
3. Your C++ program must read an input file `/home/user/requests.csv` (which contains lines formatted as `device_id_hex,timestamp_int`).
4. For each line, it must compute the correct token and output a file at `/home/user/tokens.csv` with lines formatted as `device_id_hex,timestamp_int,token_hex`.
5. Compile your program to `/home/user/fast_token_gen`.

We are simulating a massive traffic flood for vulnerability analysis, so your C++ implementation must be extremely fast. A naive bash script calling the binary will be far too slow. 

You must successfully generate valid tokens for 500,000 requests in under 0.5 seconds.