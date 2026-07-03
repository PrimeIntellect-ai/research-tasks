You are a red-team operator tasked with crafting an evasion payload to bypass a custom intrusion detection system (IDS). The IDS expects a specific token validation sequence and uses a custom payload decoder. 

You need to write a C++ program that dynamically generates this payload based on a challenge string provided by the target system.

Here are the operational parameters:
1. **Input:** The target system has placed a challenge string in the file `/home/user/challenge.txt`. Read this file to get the string (ignore any trailing newlines).
2. **Token Generation:** The IDS requires a validation token. To generate the token:
   - Take the challenge string and reverse it.
   - Base64 encode the reversed string.
3. **Payload Encoding:** The underlying payload string you need to deliver is exactly: `COMMAND:flag_captured_successfully`
   - To evade signature detection, XOR each character of this payload string with the integer value of the *length* of the original challenge string.
   - Base64 encode the resulting XORed byte array.
4. **Final Output Format:** Combine the token and the encoded payload into a single string formatted exactly as:
   `[TOKEN].[ENCODED_PAYLOAD]`
   (A period character `.` separates the two parts).

Write your C++ code to `/home/user/crafter.cpp`. 
Compile it to an executable named `/home/user/crafter`. 
When executed, your program must read `/home/user/challenge.txt` and write the final formatted string to `/home/user/evasion_payload.txt` (with or without a trailing newline).

You may use standard C++ libraries. Do not use external libraries (like OpenSSL) to keep the payload generator standalone. You will need to implement your own Base64 encoding logic within the C++ file.