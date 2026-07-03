You are a storage administrator tasked with managing disk space on a Linux server. You need to archive some legacy sensor data using a specific compression technique and maintain filesystem continuity by replacing the original files with symbolic links.

Your tasks are as follows:

1. **Locate Data**: There are several sensor log files ending in `.dat` located in `/home/user/raw_data`.
2. **Custom Compression**: Write a script in any language to compress each `.dat` file using standard `zlib` compression (default compression level). Save the compressed binary output to `/home/user/archive/` with the exact same base name but with the extension changed to `.zdat` (e.g., `sensor1.dat` becomes `sensor1.zdat`).
3. **Link Management**: Delete the original `.dat` files in `/home/user/raw_data/` and replace them with symbolic links. The symbolic links must have the exact same name as the original files (e.g., `/home/user/raw_data/sensor1.dat`), and they must point to the absolute path of their corresponding `.zdat` file in the archive.
4. **Reporting**: Create a CSV file at `/home/user/space_report.csv`. For each file processed, write a line with the following format:
   `[absolute_path_of_symlink],[absolute_path_of_compressed_target]`
   Sort the lines alphabetically by the absolute path of the symlink.

Example report line:
`/home/user/raw_data/sensor1.dat,/home/user/archive/sensor1.zdat`