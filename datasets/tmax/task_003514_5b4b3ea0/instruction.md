I am a researcher organizing a massive dataset of sensor readings, and I need your help to navigate the nested archives and extract specific anomalous data points using bash commands.

My data is packaged in an archive located at `/home/user/research_data/master_dataset.tar`. 
Inside this master archive, there are two nested archives:
1. `logs.tar.gz` - contains multi-line text logs.
2. `sensors.tar.bz2` - contains binary data files produced by the sensors.

If you extract `logs.tar.gz`, you will find a file named `experiment.log`. This file uses a multi-line format for each event, separated by a line containing exactly `--`. Here is an example of the format:

```
Timestamp: 2023-10-05 14:32:11
Event: ThermalCalibration
Status: SUCCESS
DataFile: bin_143211.dat
--
Timestamp: 2023-10-05 14:35:00
Event: CoreOverload
Status: ERROR
Error_Code: 0x88B
DataFile: bin_143500.dat
--
```

I need you to do the following:
1. Navigate and extract the nested archives.
2. Parse `experiment.log` to identify all multi-line records where the `Status` is exactly `ERROR`.
3. Extract the names of the `DataFile` fields from those specific error records.
4. Extract only those specific binary files from `sensors.tar.bz2`. 
5. Package these extracted anomaly binary files into a new archive located at `/home/user/anomalies_backup.tar.gz` (it must be a gzipped tarball containing just the files at the root level of the archive, no directories).
6. Create a text file at `/home/user/summary.txt` containing the names of the extracted binary files, sorted alphabetically, one filename per line.

You may use any standard bash CLI tools (like `grep`, `awk`, `sed`, `tar`, etc.) or write a quick script in your language of choice to accomplish this. Do not include any other files in the final backup archive.