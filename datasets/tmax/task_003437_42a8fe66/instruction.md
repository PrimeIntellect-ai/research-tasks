You are a backup administrator tasked with writing a tool to read a legacy custom archive format. 
The previous administrator left a voice memo detailing the exact binary format of these archives and the security sanitization rules required. 

Your tasks are:
1. Listen to or transcribe the audio file located at `/app/voicememo.wav` to understand the specifications of the custom archive format.
2. Write a C program that reads this custom archive format from `stdin`.
3. The program must validate the archive, parse the entries according to the audio memo, apply the path sanitization rule (to prevent zip slip vulnerabilities), and output the metadata to `stdout`.
4. Compile your program to an executable located at `/home/user/archive_tool`. 

Your tool will be tested against thousands of random and well-formed archive inputs to ensure it perfectly matches the expected behavior and security rules. If the archive is invalid (e.g., wrong magic number), the program should exit with code 1. Otherwise, it should process all entries, safely handling end-of-file conditions or truncated files by ignoring the incomplete entry and exiting with code 0.