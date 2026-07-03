You are a data engineer debugging a legacy data pipeline. A previous data scientist noticed that a silent bug was introducing NaNs into our integer dataset, causing the pandas pipeline to upcast everything to floats and ruining downstream numerical accuracy. 

Before leaving, they left an audio note describing exactly which rows are corrupted. You need to transcribe this audio, clean the data, compute its covariance, and expose the results via a high-performance C socket server.

**Requirements:**

1. **Identify Corrupted Rows:**
   Analyze the audio file located at `/app/bug_report.wav`. The speaker will mention three specific row indices (0-indexed) that contain corrupted NaN values. 

2. **Clean the Dataset:**
   The dataset is located at `/app/dataset.csv`. It contains 100 rows and 3 columns of integer data. Read this dataset and strictly filter out the three corrupted rows identified from the audio.

3. **Compute Statistics (in C):**
   Write a C program at `/home/user/data_server.c` that parses the cleaned dataset and computes the 3x3 population covariance matrix (divide by N, not N-1). 

4. **Serve the Data (Raw TCP):**
   Your C program must start a raw TCP server listening on `127.0.0.1:8080`. It must accept incoming connections and respond to the following precise ASCII commands (terminated by a newline `\n`):
   
   *   Command: `COV\n`
       Response: The 3x3 covariance matrix in row-major order. Nine space-separated numbers, formatted to exactly 3 decimal places, followed by a newline.
       *(Example: `12.345 1.000 0.000 1.000 ...\n`)*
   *   Command: `TRACE\n`
       Response: The trace of the covariance matrix (the sum of the diagonal elements, representing total variance for dimensionality reduction). A single number formatted to 3 decimal places, followed by a newline.
       *(Example: `45.678\n`)*

5. **Execution:**
   Compile your C program into `/home/user/data_server` and run it in the background so that it is actively listening on port 8080 when you finish.