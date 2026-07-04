You are an artifact manager for a high-precision manufacturing facility. Your task is to curate and analyze a repository of machine instruction files (GCode) packaged in a custom binary artifact format.

We have received a new batch of toolpaths in a custom binary archive: `/app/artifacts.bin`.
Additionally, a scanned calibration spec sheet for the target machine is located at `/app/calibration.png`.

Your objectives:
1. **Extract Calibration Data:** Read the `/app/calibration.png` image to determine the specific `X_SCALE` and `Y_SCALE` calibration multipliers for this batch.
2. **Parse Binary Archive:** Write a **C++** program that parses `/app/artifacts.bin`. The binary format is structured as follows:
    * Magic header: 4 bytes `ARTF`
    * Artifact count: 4-byte unsigned integer (little-endian)
    * Followed by `Count` artifact entries. Each entry consists of:
        * Filename length: 1-byte unsigned integer
        * Filename: ASCII string of `length` bytes
        * Payload size: 4-byte unsigned integer (little-endian)
        * Payload data: `size` bytes of raw GCode text.
3. **Analyze Toolpaths:** For each extracted GCode payload, parse the text to compute:
    * The **Bounding Box Volume**: Compute the minimum and maximum coordinates for X, Y, and Z across all `G0` and `G1` commands. *Crucial*: You must multiply all X and Y coordinates by the `X_SCALE` and `Y_SCALE` from the calibration image *before* computing the min/max and volume. Volume = `(max_X - min_X) * (max_Y - min_Y) * (max_Z - min_Z)`.
    * The **Max Extrusion**: The maximum `E` value reached in the file (assume `E` values are absolute).
4. **Generate Metrics:** Your C++ program must output a CSV file to `/app/metrics.csv` with exactly this header: `filename,volume,max_extrusion`.
    * Sort the rows alphabetically by filename.
    * Output floating point values to 4 decimal places.

To complete this task, write and compile your C++ code, execute it to process the archive, and produce `/app/metrics.csv`. You may use standard Linux command-line tools (like `tesseract` for OCR) to assist with the image extraction before feeding the values into your C++ program.