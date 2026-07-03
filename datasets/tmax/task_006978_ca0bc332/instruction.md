You are assisting a materials researcher in organizing a newly acquired dataset containing 3D printer test paths and firmware binaries. The raw data is compressed in a nested archive located at `/home/user/raw_data.zip`. 

Your objective is to extract this archive, analyze the specific domain files within it, and generate a standardized metadata summary report.

Here are your instructions:
1. Extract `/home/user/raw_data.zip`. Inside, you will find a compressed tarball named `dataset.tar.gz`. Extract this tarball as well into a directory called `/home/user/dataset`.
2. Analyze every file in `/home/user/dataset/`.
3. For files ending in `.elf` (firmware binaries):
   - Determine the machine architecture of the ELF file. Extract the exact string value provided by the `Machine:` field in the ELF header (you can use `readelf -h`).
   - Strip any leading or trailing whitespace from this value.
4. For files ending in `.gcode` (test prints):
   - Parse the text file to determine the maximum Z-height reached during the print. 
   - A Z-height is specified by the letter `Z` followed by a number (e.g., `Z15.2` or `Z0.3`) on lines that begin with a `G0` or `G1` movement command. 
   - Extract the highest numerical Z value found in the file.
5. Create a CSV summary file at `/home/user/dataset_summary.csv`.
   - The file must have the header row: `filename,type,metadata`
   - For ELF files, the `type` should be `ELF`, and the `metadata` is the machine architecture string.
   - For GCode files, the `type` should be `GCode`, and the `metadata` is the maximum Z-height (as a number).
   - The rows below the header must be sorted alphabetically by the `filename` column.

Ensure your parsing logic accurately handles the file formats and generates the exact CSV format requested.