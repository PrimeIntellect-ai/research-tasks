You are helping a developer debug a failing C++ data processing build. The project is located in `/home/user/pcap_parser`.

The application is designed to read a provided network packet capture file (`capture.pcap`), filter for UDP packets, and extract the raw application payload (a simple text message), printing it to standard output. 

Currently, the project suffers from a few issues:
1. **Failing Build**: Running `make` fails due to misconfigured environment flags and compiler/linker errors.
2. **Data Transformation Bug**: Once you get the application to compile, running `./parser capture.pcap > current_output.txt` produces an output that does not match the provided `/home/user/pcap_parser/expected_output.txt`. There is a logic error in the C++ packet parsing code related to protocol headers.

Your task:
1. Fix the `Makefile` and `main.cpp` so that the project compiles cleanly with `make`.
2. Analyze the difference between your program's output and `expected_output.txt`. Use your understanding of network packet structures to fix the C++ logic bug in `main.cpp` causing the invalid extraction.
3. Recompile and run the program against `capture.pcap`. 
4. Save the final, correct output to `/home/user/pcap_parser/final_output.txt`.

Ensure your final output exactly matches the text in `expected_output.txt`, containing only the extracted payload.