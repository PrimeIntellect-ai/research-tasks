You are assisting a researcher who is organizing experimental datasets. Instruments in the lab generate proprietary binary files and dump them continuously into a specific directory. 

Your objective is to build a robust pipeline using Bash and Go to parse these binary files, convert their character encoding, and safely save them to a processed directory.

Here are the requirements:

1. **Environment Setup**:
   - The incoming binary files will be deposited into `/home/user/datasets/raw`.
   - You must output the processed text files into `/home/user/datasets/processed`.

2. **Binary File Format**:
   Each raw `.dat` file follows this exact binary structure:
   - **Bytes 0-3**: Magic sequence `0x52 0x41 0x57 0x44` (ASCII "RAWD").
   - **Bytes 4-7**: A 32-bit Little Endian unsigned integer representing the `DatasetID`.
   - **Bytes 8-9**: A 16-bit Little Endian unsigned integer representing the Payload Length `L`.
   - **Bytes 10 to (10+L)**: The text payload, encoded in `Windows-1252` (CP1252).

3. **Processing Logic (Go)**:
   - Write a Go program at `/home/user/parser.go`.
   - It should take an input file path as a command-line argument.
   - It must read the binary file, validate the magic sequence, and extract the `DatasetID` and payload.
   - It must decode the payload from `Windows-1252` to standard `UTF-8`.
   - It must save the decoded UTF-8 text to `/home/user/datasets/processed/dataset_<DatasetID>.txt`.
   - **Atomic Writes**: To prevent researchers from reading partially written files, your Go program *must* write the output to a temporary file in the `processed` directory (e.g., appending `.tmp` to the filename) and then atomically rename it to the final `dataset_<DatasetID>.txt` filename.

4. **Automation (Bash)**:
   - Write a bash script at `/home/user/watch.sh`.
   - This script should use `inotifywait` (from `inotify-tools`) to watch the `/home/user/datasets/raw` directory for newly created or moved-in files.
   - Whenever a new `.dat` file appears, it should automatically pass it to your Go program for processing.
   - Ensure the script runs continuously (you can run it in the background to test it).

To complete the task:
1. Create the directories.
2. Write `parser.go` and `watch.sh`.
3. Start `watch.sh` in the background.
4. There is a hidden background process that will drop 3 `.dat` files into `/home/user/datasets/raw` shortly after your start. However, to prove your setup works immediately, manually create a valid binary `.dat` file matching the specification with `DatasetID = 999` and payload "Test \x80" (where \x80 is the Euro symbol € in Windows-1252), place it in the raw directory, and verify it gets processed.