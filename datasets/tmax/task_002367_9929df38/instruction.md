You are an AI assistant helping a researcher recover disorganized datasets. 

Due to a flawed log rotation script that raced with the writing process, several continuous binary sensor logs were corrupted. Valid binary records are now scattered across multiple archive files and mixed with random garbage bytes.

Your task is to extract the metadata of all valid records from specific files and create a consolidated, chronologically sorted timeline.

The dataset is located in `/home/user/sensor_archives/`.
You need to process only the files in this directory (and its subdirectories) that meet BOTH of these criteria:
1. File extension is `.log`
2. File size is strictly greater than 4096 bytes.

**Binary Record Format (Little-Endian):**
Each valid record consists of a header followed by a data payload:
- **Magic Number**: 4 bytes, `0xDEADBEEF`
- **Sensor ID**: 2 bytes, unsigned integer (`uint16_t`)
- **Timestamp**: 4 bytes, unsigned integer (`uint32_t`) representing seconds since epoch.
- **Payload Length**: 2 bytes, unsigned integer (`uint16_t`)
- **Payload**: `<Payload Length>` bytes of arbitrary binary data.

Because of the corruption, there are random bytes between valid records. The payload itself is guaranteed *never* to contain the byte sequence of the Magic Number.

**Your objectives:**
1. Write a C program at `/home/user/extractor.c` and compile it to `/home/user/extractor`.
2. The C program must read a binary stream from standard input (`stdin`).
3. It must scan the stream byte-by-byte to find the Magic Number.
4. When a Magic Number is found, it should extract the Sensor ID, Timestamp, and Payload Length, and then skip over the Payload.
5. For each valid record, the program must print a line to standard output (`stdout`) in the following exact format: `Timestamp,SensorID,PayloadLength`
6. Once your tool is compiled, find the matching files based on the metadata criteria mentioned above, pipe their concatenated contents into your C tool, and sort the resulting text output numerically by Timestamp (ascending).
7. Save the final sorted output to `/home/user/recovered_timeline.csv`.

Make sure the final output file contains only the sorted CSV data with no headers.