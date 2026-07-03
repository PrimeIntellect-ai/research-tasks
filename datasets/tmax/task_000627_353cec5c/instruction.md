You are an IT support technician responding to Ticket #4092. A researcher has reported that their legacy C++ data parsing tool, `sensor_parser.cpp`, is no longer compiling. Furthermore, even when they downgraded their compiler to make it build in the past, it was crashing on their latest dataset and calculating the wrong temperature averages.

You have been granted access to the directory `/home/user/ticket_4092` which contains:
- `sensor_parser.cpp` (the broken source code)
- `sensor_data.bin` (the binary dataset)
- `Makefile`

**Your objectives:**
1. **Fix the build failure:** Modify `sensor_parser.cpp` so that it compiles successfully using the provided `Makefile` (which runs `g++ -std=c++17 -Wall sensor_parser.cpp -o sensor_parser`).
2. **Handle corrupted input:** The binary file format expects a 4-byte ASCII magic header `SENS`. After that, each sensor record is exactly 5 bytes:
   - A 1-byte marker that MUST be `0xFF`.
   - A 2-byte unsigned integer for Sensor ID (little-endian).
   - A 2-byte signed integer for Temperature in deci-Celsius (little-endian).
   Due to a transmission glitch, `sensor_data.bin` contains corrupted bytes between some valid records. If a marker byte is not `0xFF`, the parser currently throws an exception and crashes. You must modify the code to catch/handle this by advancing byte-by-byte until the next valid `0xFF` marker is found, allowing it to recover and read the remaining valid records.
3. **Correct the formula:** The program calculates the average temperature. The formula currently implemented has a logical error: it performs integer division and forgets to scale the deci-Celsius values to actual Celsius (e.g., 215 deci-Celsius = 21.5 C). Fix the logic so the average is a correct floating-point value in Celsius.
4. **Output the results:** Make the fixed program output its final results to `/home/user/ticket_4092/report.txt`.

**Output Format for `report.txt`:**
The file must contain exactly two lines:
```
Average Temperature: <value> C
Valid Records: <count>
```
*(Format the average temperature to exactly 2 decimal places).*

Fix the code, compile it, run it on `sensor_data.bin`, and ensure `report.txt` is generated correctly.