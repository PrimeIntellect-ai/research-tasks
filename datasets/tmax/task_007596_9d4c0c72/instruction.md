You are an IT support technician resolving Ticket #8022. 

A user's local analytics script is failing to converge, throwing an error, and producing no output. The user also accidentally deleted their configuration file from their USB drive image, and the backend server that usually provides the data is offline. Fortunately, the user attached a network packet capture of the last successful data fetch.

You have the following files in `/home/user/ticket8022`:
1. `model.py`: The Python script that runs an iterative algorithm. It is currently crashing/diverging.
2. `usb.img`: An unmounted ext4 filesystem image. The user deleted `config.json` from the root of this drive.
3. `traffic.pcap`: A packet capture containing an HTTP response from the backend server with the required JSON data payload.

Your tasks:
1. **Recover the configuration:** Inspect the filesystem image `usb.img` to recover the contents of the deleted `config.json`. Do not attempt to mount the image using `sudo` or `mount`, as you do not have root privileges. (Hint: ext4 filesystem debugging tools can read unmounted images). Note the `learning_rate` inside.
2. **Extract the data:** Analyze `traffic.pcap` to find the HTTP response body containing a JSON array of data points.
3. **Fix the script:** 
   - `model.py` is hardcoded to use a dummy learning rate and dummy data. Update it to use the recovered `learning_rate` and the extracted data array.
   - The script is currently failing to converge due to a bad data point (an anomalous negative value representing a sensor error). Modify `model.py` to filter out any negative values before running the optimization loop.
4. **Run the script:** Execute the fixed `model.py`. It will print a final converged value.

Save a final report to `/home/user/ticket8022/report.txt` in the following exact format:
```
LEARNING_RATE: <recovered_learning_rate>
DATA_POINTS: <number_of_valid_data_points_after_filtering>
CONVERGED_VALUE: <rounded_to_4_decimal_places>
```