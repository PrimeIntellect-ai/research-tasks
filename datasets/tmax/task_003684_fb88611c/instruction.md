You are a performance engineer investigating a sudden spike in processing latency for a legacy data pipeline. The source code for the metric parser was accidentally deleted, but the compiled bytecode remains. Furthermore, the binary metrics file you collected was corrupted during transmission.

Your task is to reverse-engineer the parsing logic, recover the corrupted binary data, and perform a statistical anomaly investigation to isolate the root cause.

Here are the details:
1. **Binary Reverse Engineering**: 
   You will find a compiled Python bytecode file at `/home/user/reader.pyc`. It contains a function `get_struct_format()` which returns the Python `struct` format string used to pack the binary records. You must inspect this bytecode (e.g., using Python's `dis` module) to extract the format string. The records consist of three fields in this exact order: `ID` (integer), `Timestamp` (float), and `Latency` (float).

2. **Corrupted Input Handling**:
   The binary file `/home/user/corrupted_metrics.dat` contains the packed records. However, a known network bug periodically injected a corruption marker: the exact 4-byte sequence `0xDE 0xAD 0xBE 0xEF` (represented as an unsigned 32-bit little-endian integer), immediately followed by exactly 4 bytes of garbage. 
   You must read the file, identify and skip these 8-byte corrupted sequences (the marker + the 4 garbage bytes), and parse the rest of the stream sequentially to recover all valid records.

3. **Statistical Anomaly Investigation**:
   Once you have successfully extracted all the valid records, calculate the mean and sample standard deviation of the `Latency` values across the entire dataset.
   Define an anomaly as any record where the latency is strictly greater than `Mean + (3 * Standard Deviation)`.
   Identify the `ID` associated with the highest maximum latency among these anomalous records.

**Deliverable**:
Create a file at `/home/user/anomaly_report.txt` containing exactly the following four lines, replacing the bracketed placeholders with your findings. Format the floats to exactly two decimal places.

```
Format: <extracted_struct_format_string>
Mean: <mean_latency>
StdDev: <std_dev_latency>
TargetID: <anomalous_id>
```