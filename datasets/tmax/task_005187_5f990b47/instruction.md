You are a data analyst taking over a C-based data processing service. The previous engineer was building a TCP microservice for our ETL pipeline but left behind a critical flaw: the data pipeline leaks information between the training and testing sets during standard scaling.

Your objective is to fix the pipeline, extract missing calibration data from an image, and deploy the corrected C service.

1. **Extract Calibration Data**: 
   There is an image at `/app/calibration.png` containing a single text string: `CALIBRATION_MULTIPLIER=X.XX`. Use OCR (e.g., `tesseract`) to extract this multiplier.

2. **Develop the ETL TCP Service in C**:
   Write a C program that listens for TCP connections on `127.0.0.1:9000`. You may use standard libraries and `libgsl` (GNU Scientific Library) for numerical operations. 

   When the server receives a request in the format `EVAL <N>\n` (where `<N>` is an integer representing the split index), it must perform the following:
   
   a) Load the dataset from `/home/user/sensor_data.csv` (a single column of raw floating-point values).
   b) Multiply every value in the dataset by the extracted `CALIBRATION_MULTIPLIER`.
   c) Split the dataset: indices `0` to `<N>-1` are the **training** set; indices `<N>` to the end of the file are the **testing** set.
   d) **Prevent Data Leakage**: Standardize the data. Calculate the mean and standard deviation of the **training** set. Standardize the **testing** set using the *training* mean and standard deviation (i.e., `scaled_test[i] = (test[i] - train_mean) / train_std`). 
   e) **Bootstrap Analysis**: Perform bootstrap sampling on the `scaled_test` set to estimate the 95% confidence interval of its mean. Generate 1000 resamples (with replacement) of the scaled test set using GSL's random number generators. Calculate the mean of each resample, sort the means, and extract the 2.5th and 97.5th percentiles.
   
3. **Response Format**:
   For each `EVAL <N>\n` request, the server must calculate the above and respond over the TCP connection with the exact string:
   `CI: <lower>, <upper>\n`
   (Format the floats to exactly 4 decimal places, e.g., `CI: -0.1234, 0.5678\n`). The server should then close the client connection but continue listening for new requests.

Ensure your C program compiles and runs continuously in the background, listening on port 9000, before you conclude the task.