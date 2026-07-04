I am a climate researcher organizing a massive, messy dataset of sensor readings, and I need your help to parse and restructure the data. 

I have an archive located at `/home/user/climate_raw.tar.gz`. Inside this archive is a deep directory structure containing hundreds of gzipped data logs (files ending in `.dat.gz`).

The data inside these `.dat.gz` files is plain text, but it is heavily unstructured. Each line looks exactly like this:
`[YYYY-MM-DD HH:MM:SS] - SENSOR_<ID> - <EVENT_TYPE> - <VALUE>`

Here is what I need you to do:
1. Extract the tarball `/home/user/climate_raw.tar.gz`.
2. Find all `.dat.gz` files and process them. You must read them as compressed streams (without extracting the inner `.dat.gz` files to disk to save space).
3. Filter the data to find only lines where the `<EVENT_TYPE>` is exactly `OZONE_SPIKE` and the `<VALUE>` (which is a floating-point number) is strictly greater than `150.0`.
4. Transform the matched lines into a clean CSV format: `YYYY-MM-DD,HH:MM:SS,SENSOR_<ID>,<VALUE>`
5. Route these parsed lines into new CSV files based on the sensor ID. Create a directory `/home/user/clean_data/`. For every sensor that has a matched anomaly, create a file named `<SENSOR_NAME>.csv` inside this directory (e.g., `SENSOR_Alpha.csv`).
6. Each CSV file must have exactly this header as its first line: `Date,Time,Sensor,OzoneLevel`. Ensure the header only appears once per file at the top.
7. Once all data is parsed and written, package the entire `/home/user/clean_data` directory into a new XZ-compressed tarball located at `/home/user/clean_data.tar.xz`.
8. Create a simple text file at `/home/user/summary.txt` containing only a single integer: the total number of `OZONE_SPIKE` anomalies > 150.0 found across all files.

You can use any programming language (Python, Bash, awk, etc.) available in a standard Linux environment to accomplish this. Please ensure all file paths strictly match the ones requested.