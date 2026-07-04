You are helping a developer migrate a backend data processing pipeline from Python 2 to Python 3. 

The Python service intercepts incoming REST API requests and dumps the structured payloads to disk in a custom binary format. These dumps are then parsed by a highly optimized C utility. During the migration to Python 3, changes in how strings and bytes are handled mean that the payload length occasionally exceeds the C utility's fixed buffer sizes, leading to segmentation faults.

The vulnerable C parser is located at `/home/user/api_parser.c`. 
The binary format is simple: the very first byte represents the length of the payload `L`, followed by `L` bytes of data.

Your task:
1. Identify the buffer overflow vulnerability in `/home/user/api_parser.c`. The `buffer` is exactly 50 bytes long.
2. Modify `/home/user/api_parser.c` to cap the copied length to 49 bytes (to leave room for the null terminator). If the length byte `L` is greater than 49, the program should only copy 49 bytes from the payload into the buffer.
3. Compile the updated C code to `/home/user/api_parser` using `gcc`.
4. Apply the concept of property-based testing by writing a simple bash fuzzer. Create a bash script at `/home/user/fuzz.sh` that:
   - Generates a file `/home/user/test.bin` containing a single byte with the value `255` (0xFF), followed by 255 random bytes (you can use `/dev/urandom` and `head`).
   - Executes `/home/user/api_parser /home/user/test.bin`.
   - If the C program exits cleanly (exit code 0), write the word `SUCCESS` to `/home/user/fuzz_result.log`.
5. Execute `/home/user/fuzz.sh` to generate the log file.

Ensure the final compiled binary and the log file exist at the exact paths specified.