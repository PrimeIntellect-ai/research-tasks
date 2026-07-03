You have just inherited an unfamiliar C codebase located at `/home/user/sensor_project`. This project is responsible for parsing a proprietary binary sensor data file (`data.bin`) and calculating the statistical mean of the sensor readings.

However, the current state of the project is broken:
1. **Secret Recovery:** The decryption key required to decode the payload was accidentally removed from `process.c` in a recent commit. You need to investigate the Git history of the repository to find the lost 32-bit `SECRET_KEY` and restore it in the code.
2. **Corrupted Input Handling:** The binary file `data.bin` occasionally contains corrupted records with excessively large payload lengths. The current C program crashes (Segmentation Fault) because it blindly reads the payload into a fixed-size 64-byte buffer. You must debug and fix the C code to gracefully skip any record where the length exceeds 64 bytes, without crashing and without losing track of the file pointer.
3. **Statistical Anomaly:** Once the key is restored and the memory corruption bug is fixed, compiling and running the program should process the valid data and print the mean. 

Your tasks:
- Recover the `SECRET_KEY` from the Git history and insert it into `process.c`.
- Fix the buffer overflow bug in `process.c` so that it skips over records with a length greater than 64 bytes (i.e., advance the file pointer by the indicated length and move to the next record).
- Compile the fixed program (e.g., `gcc process.c -o process`).
- Run the program and redirect its standard output to `/home/user/result.txt`.

The output written to `/home/user/result.txt` must strictly be in the format:
`Anomaly Mean: <value>`

Everything you need is in `/home/user/sensor_project`. Good luck!