You are an authorized penetration tester analyzing a proprietary authentication service. The service uses a weak custom token generation algorithm.

You have obtained the source code for the token generation function, located at `/home/user/pentest/token_gen.c`. 
You have also intercepted an authentication token generated for the user `admin`, which is saved in `/home/user/pentest/captured_token.txt`.

The token is generated using a 4-digit PIN (ranging from 0000 to 9999) combined with the username.

Your objective is to:
1. Analyze the token generation algorithm in `/home/user/pentest/token_gen.c`.
2. Write a C program to brute-force the 4-digit PIN used to generate the `admin` token found in `/home/user/pentest/captured_token.txt`.
3. Save the cracked 4-digit PIN (e.g., `1234`) to `/home/user/pentest/cracked_pin.txt`.
4. Use the cracked PIN and the algorithm to generate a new, valid authentication token for the user `root`.
5. Save this new `root` token in hexadecimal format (e.g., `0x1a2b3c4d`) to `/home/user/pentest/root_token.txt`.

You may write your brute-force and token generation code in C, and compile/run it using the standard GCC toolchain available on the system.