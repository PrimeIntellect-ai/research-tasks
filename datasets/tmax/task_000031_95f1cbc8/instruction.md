You are an AI assistant helping a data science researcher process laboratory logs. 

The researcher has recorded their experimental observations in an audio log located at `/app/lab_log_12.wav`. The audio contains spoken data points for an experiment, dictating pairs of variables ("alpha" and "beta") for several observations. 

Your task is to build a complete data pipeline that transcribes this audio, extracts the numeric dataset, performs statistical analysis, and serves the results over a network API. 

Here are your specific requirements:

1. **Environment Setup & Transcription:**
   - Install any necessary transcription tools (e.g., whisper, ffmpeg, or python packages) to transcribe the audio file at `/app/lab_log_12.wav`.
   - Tokenize and extract the paired numeric values for "alpha" (the independent variable, X) and "beta" (the dependent variable, Y). 
   - Enforce a strict data schema: discard any observations where either variable is missing, non-numeric, or explicitly stated as "invalid" or "error".

2. **Statistical Modeling & Bootstrap (Primary Implementation in C):**
   - Write a C program (`/home/user/analyzer.c`) that reads the extracted dataset.
   - The C program must perform a simple linear regression (Ordinary Least Squares) to find the slope (beta coefficient) predicting "beta" from "alpha".
   - The C program must also implement a Bootstrap sampling method (with at least 1,000 resamples) to compute the 95% confidence interval for this slope.

3. **Data Serving (Multi-protocol Integration):**
   - Your C program must launch an HTTP server listening on `0.0.0.0:8080`.
   - The server must respond to HTTP GET requests and require the following authentication header: `Authorization: Bearer RES-994`. If this header is missing or incorrect, return a `401 Unauthorized` status.
   - Implement two endpoints:
     - `GET /data`: Returns the cleaned, tokenized dataset as a JSON array of objects (e.g., `[{"alpha": 1.0, "beta": 2.1}, ...]`).
     - `GET /stats`: Returns the statistical results as a JSON object containing the keys `"slope"`, `"bootstrap_ci_lower"`, and `"bootstrap_ci_upper"`.

You may use auxiliary scripts (e.g., Python or bash) to handle the audio transcription and feed it to your C program, but the data schema enforcement, statistical calculations, and the HTTP server *must* be implemented in C. Once your server is running, leave it running in the background so it can be verified.