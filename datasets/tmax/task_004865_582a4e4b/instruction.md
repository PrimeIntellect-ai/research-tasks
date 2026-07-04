You are an engineer tasked with investigating a severe memory leak and hang in our data processing daemon. 

Our daemon (`/home/user/service.py`) uses a C library (`/home/user/libparser.so`, source at `/home/user/parser.c`) to parse incoming binary telemetry payloads. Intermittently, the service processes a payload that causes it to hang indefinitely while consuming unbounded amounts of memory.

Yesterday, the service hung while processing a payload saved at `/home/user/last_input.dat`. Unfortunately, a cleanup cron job deleted `/home/user/last_input.dat` from the filesystem. However, a monitoring script running `tail -f /home/user/last_input.dat` in the background was active when the file was deleted, meaning the file descriptor is still open.

Your tasks:
1. **Recover the deleted payload:** Recover the contents of the deleted `last_input.dat` using the running `tail` process. Save the exact recovered binary data to `/home/user/recovered_payload.dat`.
2. **Fix the memory leak/hang:** Inspect `/home/user/parser.c`. There is a loop termination/state bug that causes an infinite loop and unbounded memory allocation when parsing the recovered payload. Fix the bug in `/home/user/parser.c` so that it correctly parses the malformed data without hanging, and properly increments the parsing index.
3. **Recompile the library:** Recompile the C library using: `gcc -shared -o /home/user/libparser.so -fPIC /home/user/parser.c`
4. **Fuzz / Verify:** We have provided a fuzzing script at `/home/user/fuzzer.py` that generates variations of payloads. Run the fuzzer to ensure the service no longer hangs. Finally, process the recovered payload using the fixed service:
   `python3 /home/user/service.py /home/user/recovered_payload.dat > /home/user/fix_verified.log`

The automated test will verify:
- The existence and exact contents of `/home/user/recovered_payload.dat`.
- That `/home/user/fix_verified.log` exists and contains the success message "Parse complete: 256 bytes".
- That running `python3 /home/user/fuzzer.py` completes without hanging or crashing.