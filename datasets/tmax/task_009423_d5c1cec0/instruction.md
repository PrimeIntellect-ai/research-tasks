You are an AI assistant helping a scientific researcher organize and process a legacy dataset. 

The researcher has an archive of sensor data located at `/home/user/sensor_data.raw.gz`. You need to write a Rust command-line tool that processes this gzipped binary stream, extracts specific records based on their binary headers, and outputs the results.

### Data Format Specification
The file `/home/user/sensor_data.raw.gz` is a Gzip-compressed stream containing a sequence of concatenated binary records. 
Each uncompressed record has the following binary format (all multi-byte integers are in **Big Endian** byte order):
1. **Magic Bytes**: 4 bytes, always the ASCII characters `SENS` (0x53, 0x45, 0x4E, 0x53).
2. **Sensor ID**: 2 bytes, unsigned 16-bit integer (`u16`).
3. **Timestamp**: 8 bytes, unsigned 64-bit integer (`u64`).
4. **Payload Length**: 2 bytes, unsigned 16-bit integer (`u16`).
5. **Payload Data**: Variable length (exactly the number of bytes specified by the Payload Length field).

### Your Objectives

1. **Create a Rust Project**:
   Initialize a new Rust binary project named `sensor_parser` in `/home/user/sensor_parser`.

2. **Write the Parsing Logic**:
   Write the Rust program to read the **compressed** data directly from `stdin`. You must decompress the stream on the fly within your Rust application (e.g., using the `flate2` crate) and process the uncompressed binary data.
   
3. **Filter and Extract**:
   Parse the binary records sequentially. 
   Filter the records to keep ONLY those where the **Sensor ID** is exactly `42`.

4. **Output Requirements**:
   For each record that matches Sensor ID 42, print a single line to standard output (`stdout`) in the exact following format:
   `Timestamp: <timestamp>, Payload: <hexadecimal string of the payload>`
   *(Note: The hex string must be lowercase and have no spaces or prefixes like "0x".)*

5. **Execution**:
   Build your Rust application in release mode.
   Run it by piping the input file directly into your application and redirecting the output to a log file:
   `cat /home/user/sensor_data.raw.gz | ./target/release/sensor_parser > /home/user/extracted_sensor_42.log`

Verify your logic carefully. The binary stream might have adjacent records immediately following the payload of the previous record. The program should terminate cleanly when the EOF is reached.