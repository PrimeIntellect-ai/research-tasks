You are tasked with analyzing a legacy configuration and telemetry export from an industrial control system. The system logs its temperature sensor data directly into an uncompressed audio file (WAV format) and exports its configuration constraints in a legacy binary format. 

Your objective is to decode the metadata, clean the telemetry data, and detect the exact index of a critical system state change.

1. **Process the Metadata:**
   The file `/app/metadata.dat` contains the sensor configuration metadata in JSON format, but it was exported using IBM EBCDIC `cp500` character encoding. Read and decode this file. It contains the keys `min_valid` and `max_valid`.

2. **Extract and Clean the Audio Telemetry:**
   The file `/app/telemetry.wav` is a 16-bit mono PCM WAV file. The audio sample rate is extremely low (10 Hz). Every individual sample (frame) represents a raw temperature reading at that tick.
   Read the audio samples into an array/list of integers.
   Apply constraint-based validation: The sensor occasionally glitches and records extreme values. Any sample value that is strictly less than `min_valid` or strictly greater than `max_valid` is invalid. You must clean the data by replacing any invalid sample with the *most recent valid sample* before it. (Assume the first sample in the file is always valid).

3. **Detect the Changepoint:**
   After cleaning the constraints, you must perform changepoint detection to find a sudden anomaly in the operational state. At some specific sample index, the baseline temperature shifts dramatically upwards and stays there. 
   Find the sample index where this sustained baseline shift occurs.

4. **Output:**
   Create a file at `/home/user/result.json` with the following exact format:
   ```json
   {
       "changepoint_index": 1234
   }
   ```
   Replace `1234` with your detected integer index.