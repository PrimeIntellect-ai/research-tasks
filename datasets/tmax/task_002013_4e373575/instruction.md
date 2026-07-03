You have inherited an unfamiliar legacy data processing pipeline for an IoT sensor network. The previous developer left abruptly, and the system is currently failing intermittently. 

At the core of the pipeline is a compiled C binary located at `/app/ingest.bin`. This binary parses `.dat` telemetry files, but it intermittently crashes (Segmentation Fault) on certain malformed inputs. 

You need to build a sanitization script that filters out these malformed "poison" files before they reach the binary, but the source code for `ingest.bin` is missing.

Here is what you have:
1. `/app/ingest.bin`: The legacy binary. It takes a single file path as an argument.
2. `/app/legacy_data.img`: An ext4 filesystem image (accessible via user-space tools like `debugfs` or `sleuthkit`) from the previous developer's machine. They accidentally deleted their test corpus, but the deleted `.dat` files are still recoverable from this image. Recover them to use as your local test cases.
3. `/app/struct_spec.png`: A scanned snippet of the original engineering notebook. It contains handwritten notes about the binary's internal memory layout and packet structure. You will need to extract the information from this image to understand the binary's parsing logic.

Your Task:
1. Recover the deleted test files from `/app/legacy_data.img`.
2. Analyze the image at `/app/struct_spec.png` to understand the telemetry packet schema.
3. Use a debugger (`gdb`), delta debugging, or reverse engineering on `ingest.bin` alongside the recovered files to identify the exact byte conditions that cause the crash.
4. Write a multi-language filter (preferably Python) at `/home/user/filter.py`.

Your script `/home/user/filter.py` must take exactly one command-line argument: a path to a directory containing `.dat` files. 
It must inspect all `.dat` files in that directory and print to `stdout` the **basenames** (e.g., `sensor_44.dat`) of only the "clean" files that are SAFE to process and will NOT cause `ingest.bin` to crash. Do not print the names of the files that will cause a crash. Print one filename per line.

Ensure your script is perfectly accurate. It will be tested against a hidden, adversarial corpus of clean and evil files.