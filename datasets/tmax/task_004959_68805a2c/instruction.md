You are an artifact manager responsible for curating binary repositories. We have received a nested archive of proprietary binary artifacts, and we need to extract metadata from their headers to catalog them properly.

Your task is to:
1. Extract the nested archive located at `/home/user/artifacts.tar.gz`. It contains multiple inner tarballs, which in turn contain `.bin` artifact files.
2. Write a C program to parse the custom binary header of every `.bin` file found. 
3. The custom binary header format for each `.bin` file is strictly defined as follows (little-endian where applicable):
   - Offset 0x00 (4 bytes): Magic number. Must be exactly the ASCII string "ARTI" (0x41 0x52 0x54 0x49).
   - Offset 0x04 (2 bytes): Artifact Version (unsigned 16-bit integer).
   - Offset 0x06 (2 bytes): Description Length (unsigned 16-bit integer).
   - Offset 0x08 (variable): Description (ASCII string of length equal to the Description Length. It is NOT null-terminated in the file).
4. Run your C program (or a shell script using it) to process all `.bin` files extracted from the archive.
5. Generate a report file at `/home/user/artifact_report.csv`. 
   - The CSV must have the exact header: `filename,version,description`
   - Include only the base filename (e.g., `alpha.bin`, not the full path).
   - The rows must be sorted alphabetically by the `filename` column.
   - Ignore any `.bin` files that do not start with the correct "ARTI" magic number.

Provide your solution by executing the necessary commands, writing the C code, compiling it, and generating the `/home/user/artifact_report.csv` file.