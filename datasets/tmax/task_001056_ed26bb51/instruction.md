As a data analyst, you must process an acoustic sensor recording of a manufacturing machine to detect anomalies and correlate them with machine logs.

You have been provided with:
1. `/app/sensor_audio.wav`: A mono, 8000Hz, 16-bit PCM WAV file containing the acoustic recording of the machine run.
2. `/app/machine_logs.csv`: A CSV file containing standard operating logs (Columns: `Timestamp_sec`, `Machine_State`, `Batch_ID`).

Your task:
1. Extract the amplitude data from `/app/sensor_audio.wav` into a readable format (e.g., using `sox` or `ffmpeg` to output a CSV/TXT).
2. Write a C++ program (`/home/user/detector.cpp`) that acts as a pipeline step to process the extracted audio data. It must implement a simple changepoint/anomaly detection: flag any point where the absolute amplitude exceeds 0.8 (normalized from -1.0 to 1.0, or equivalent > 26214 in 16-bit PCM) for at least 5 consecutive samples. Record the start timestamp (in seconds) of each anomaly.
3. Your C++ program should output a CSV named `/home/user/anomalies.csv` with the column `Anomaly_Time_sec`.
4. Perform a join between `/home/user/anomalies.csv` and `/app/machine_logs.csv` using shell tools. Match each anomaly to the closest log entry within a 1.0-second window. Apply a quality gate: drop any anomalies that do not match a log entry. 
5. Output the final stratified sample of anomalies into `/home/user/final_report.csv` containing columns: `Anomaly_Time_sec,Machine_State,Batch_ID`.

The automated test will evaluate `/home/user/final_report.csv` by calculating the Mean Squared Error (MSE) of the `Anomaly_Time_sec` values against a hidden ground-truth reference array.