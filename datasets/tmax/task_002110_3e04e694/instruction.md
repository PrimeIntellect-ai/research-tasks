You are assisting a technical writer in organizing documentation for a large 3D printing farm. The writer needs an automated way to extract metadata from large GCode files to build a documentation index.

In the `/home/user/doc_repo` directory, there is a configuration file named `config.ini` which lists the 3D models and the relative paths to their corresponding GCode files. 

Your task is to write and execute a Python script at `/home/user/build_index.py` that does the following:
1. Parses `/home/user/doc_repo/config.ini` to find the GCode files.
2. Efficiently reads each GCode file. Since these files can theoretically be hundreds of megabytes, you must use streaming (line-by-line reading) or memory-mapped I/O rather than loading the entire file into memory at once.
3. Parses the GCode format to extract:
   - **MaxTemp**: The highest target hotend temperature. Look for `M104 S<temp>` or `M109 S<temp>` commands and find the maximum integer temperature specified.
   - **TotalLayers**: The total number of layers, which is specified exactly once in the file as a comment in the format `; LAYER_COUNT:<count>`.
4. Writes the results to `/home/user/doc_repo/index.csv`. To ensure that documentation readers never see a partially written file, you **must** use an atomic write: write the output to a temporary file in the same directory first, and then atomically replace/rename it to `index.csv`.

The output `/home/user/doc_repo/index.csv` must be a CSV file with the exact header `Model,MaxTemp,TotalLayers`. The rows must be sorted alphabetically by the `Model` name. If a value is missing in the GCode, output `None` for that field.

Ensure you run your script so the final `index.csv` is generated before you finish.