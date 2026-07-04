You are a backup administrator tasked with migrating modern JSON backup metadata into a legacy archiving appliance. The legacy system has strict requirements for character encoding, structured data format (CSV), and file chunking. The exact configuration parameters for this appliance were recorded in a video tutorial, specifically embedded as a subtitle track within the video.

Your task has two parts:

1. **Extract Requirements**:
   Examine the video file located at `/app/archive_feed.mp4`. The video contains a subtitle track (metadata stream) that specifies two configuration variables: `CHUNK_SIZE` and `ENCODING`. Extract these values.

2. **Write the Converter**:
   Write a Python script at `/home/user/format_backup.py` that processes the backup manifests according to those variables. The script must:
   - Read a single JSON array of objects from `standard input` (`sys.stdin.read()`).
   - Each JSON object will contain the keys: `filename`, `size_bytes`, and `checksum`.
   - Convert this JSON data into CSV format. The CSV must have the exact header: `filename,size_bytes,checksum`.
   - Chunk the data: the output must be split into chunks of exactly `CHUNK_SIZE` data records (as defined in the video). 
   - Every chunk must begin with the CSV header.
   - Chunks must be separated by a single line containing exactly `---SPLIT---`.
   - Encode the final combined text into the character encoding specified by `ENCODING` in the video.
   - Write the resulting raw bytes directly to `standard output` (`sys.stdout.buffer.write()`).

*Example of conceptual text output (before encoding) for CHUNK_SIZE=2:*
```
filename,size_bytes,checksum
backup1.tar,1024,abc
backup2.tar,2048,def
---SPLIT---
filename,size_bytes,checksum
backup3.tar,4096,ghi
```

Ensure your script handles edge cases, such as an empty JSON array (which should just output the encoded header), and correctly escapes any CSV special characters if they appear in filenames.