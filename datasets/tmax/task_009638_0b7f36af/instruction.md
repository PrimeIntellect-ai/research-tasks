You have inherited an unfamiliar codebase for a sensor logging system. The previous developer left behind a C program `/home/user/sensor_logger.c` and a binary `/home/user/sensor_logger`.

The program is supposed to append 10-byte binary records to a database file. However, it intermittently crashes when receiving negative sensor values. A recent crash has corrupted the end of the database file located at `/home/user/data/sensor.db`.

Your tasks are:
1. Debug and fix the C program `/home/user/sensor_logger.c`. It must correctly log negative values without crashing or leaking memory. Recompile the fixed program to `/home/user/sensor_logger` (use `gcc -g -o sensor_logger sensor_logger.c`).
2. Analyze `/home/user/data/sensor.db`. The file consists of an append-only sequence of records. Each valid record is exactly 10 bytes long and contains:
   - `timestamp` (unsigned 32-bit integer, little-endian)
   - `sensor_id` (unsigned 16-bit integer, little-endian)
   - `value` (signed 32-bit integer, little-endian)
   The recent crash left a partial, corrupted record at the end of the file.
3. Extract all fully intact, valid records from `/home/user/data/sensor.db` and write them to `/home/user/data/recovered.csv`. The CSV should have no header and use the format: `timestamp,sensor_id,value`.

Ensure your fixed binary does not crash when run with: `./sensor_logger 1600000000 1 -50`