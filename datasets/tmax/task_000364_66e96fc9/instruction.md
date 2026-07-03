**IT Support Ticket: #9924 - Edge Node Crash & Anomaly Recovery**

**From:** Dr. Aris (Data Science Team)
**Subject:** Urgent: Recover corrupted sensor journal and identify anomalies

Hello IT Support,

Our edge monitoring node crashed hard due to a power supply failure. The main database is completely toast, but we managed to salvage the raw transaction journal file at `/home/user/sensor.journal`. Unfortunately, it's partially corrupted—there are null bytes, truncated lines, and garbage binary characters mixed in with the valid JSON lines. 

Furthermore, we lost the `config.json` that contained the calibration multipliers for the sensors. The only backup of these calibration factors is a screenshot of the old dashboard I had saved on my desktop, which has been uploaded to the server at `/app/calibration_matrix.png`.

We need you to process this data and identify the anomalies. Here is your workflow:

1. **Extract Calibration Factors:** Use OCR to read `/app/calibration_matrix.png`. You will find three sensors and their corresponding numerical calibration multipliers.
2. **Data Recovery:** Read through `/home/user/sensor.journal`. You need to recover all intact, valid lines that look like `{"timestamp": <int>, "sensor": "<string>", "raw_value": <float>}`. Discard any line that does not strictly conform to this JSON schema or contains binary garbage.
3. **Data Correction:** For every recovered reading, calculate the `corrected_value` by multiplying the `raw_value` by the sensor's calibration multiplier found in step 1.
4. **Statistical Anomaly Detection:** For each sensor independently, compute the population mean and population standard deviation of its `corrected_value`s. Identify all readings where the absolute Z-score of the `corrected_value` is strictly greater than 2.5. 
    * *Formula:* `Z = (corrected_value - mean) / std_dev`
5. **Output:** Write the identified anomalous records to `/home/user/anomalies.csv`. 
    * The CSV must have a header: `timestamp,sensor,corrected_value`
    * The `corrected_value` should be rounded to 2 decimal places.
    * Sort the CSV by `timestamp` in ascending order.

Please get this done as soon as possible so we can figure out what caused the power surge. You can write scripts in any language you prefer to automate this process.

Thanks,
Aris