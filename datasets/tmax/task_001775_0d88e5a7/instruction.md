I have a compressed tar archive `/home/user/prints.tar.gz` containing various project files, including some `.gcode` files for my 3D printer. I suspect the archive was packaged maliciously by a third party and contains directory traversal paths (like `../../`) that might overwrite system files if extracted normally (a Zip Slip attack).

To be safe, I want to organize and inspect the data *without* extracting the files to disk. 

Please process the compressed archive stream directly. Find all the `.gcode` files inside it, and extract every line that begins exactly with `M109` (the GCode command to set extruder temperature and wait). 

Save the results to `/home/user/temperatures.log`. Each line in the log must be formatted exactly as:
`<basename>: <matched_line>`
where `<basename>` is the filename of the `.gcode` file without any leading directories, and `<matched_line>` is the exact line from the file.

Constraints:
- Do not extract the files to disk. All processing must be done in-memory via streams/pipes.
- Only process files ending in `.gcode`.
- Preserve the exact spacing of the matched line, but remove carriage returns (`\r`) if present.