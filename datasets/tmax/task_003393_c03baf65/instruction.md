You are tasked with recovering and analyzing data for a 3D printer farm's Configuration Manager. The system tracks firmware updates and print jobs but recently suffered a partial filesystem corruption.

Your objective is to use Python to merge fragmented print job files, handle character encoding inconsistencies, parse a custom Write-Ahead Log (WAL) to find the latest firmware, and extract metadata from the corresponding Executable and Linkable Format (ELF) firmware file.

Complete the following steps:

1. **Merge and Convert GCode Fragments:**
   - The directory `/home/user/gcode_parts` contains several fragmented GCode files named `print.gcode.part1`, `print.gcode.part2`, etc.
   - These parts were saved using different character encodings due to a misconfiguration (they may be `utf-8`, `utf-16le`, or `windows-1252`).
   - Write a Python script to read these parts in their correct numerical order, decode them properly, and merge them into a single UTF-8 encoded file at `/home/user/merged_print.gcode`.
   - Parse the merged GCode file and calculate the total extrusion. The total extrusion is the sum of all numerical values following the `E` parameter in `G1` commands (e.g., for `G1 X10 Y10 E1.5`, add 1.5).

2. **Parse the Configuration WAL:**
   - The file `/home/user/config_manager.wal` is a custom text-based Write-Ahead Log tracking system changes.
   - Format of each line: `[TIMESTAMP] | ACTION | FILEPATH | STATUS`
   - Find the most recent (latest timestamp) entry where the `ACTION` is `FIRMWARE_UPDATE` and the `STATUS` is `SUCCESS`.
   - Identify the `FILEPATH` of the ELF firmware file from this entry.

3. **Extract ELF Metadata:**
   - The identified firmware file is a standard Linux ELF binary.
   - Extract its Entry Point address (in hexadecimal format, exactly as formatted by standard tools, e.g., `0x401120`). You may use command-line tools like `readelf` or Python libraries like `pyelftools`.

4. **Generate Final Report:**
   - Create a JSON report at `/home/user/report.json` containing the exact following structure:
     ```json
     {
       "latest_firmware_path": "<extracted_filepath>",
       "firmware_entry_point": "<extracted_entry_point_hex>",
       "total_extrusion": <float_sum_of_E_values>
     }
     ```

Ensure all dependencies you need are installed via `pip` or `apt` if they are not already present. You must rely on Python to perform the merging, encoding conversion, and parsing logic, though you may invoke shell commands from within Python or your terminal.