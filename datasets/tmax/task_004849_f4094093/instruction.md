You are a data engineer building a lightweight ETL pipeline for an IoT monitoring system. You have received a batch of time-series log data from legacy sensors.

The raw data is located at `/home/user/data/raw_logs.tsv`. 
It is a Tab-Separated Values (TSV) file with no header. Each line has exactly three columns:
1. **Timestamp**: A Unix epoch integer.
2. **SensorID**: A short alphanumeric string.
3. **Payload**: A hex-encoded string representing the raw text message sent by the sensor.

Your task is to create a C-based pipeline that extracts a specific feature from this data: the count of valid words in the decoded payload.

Requirements:
1. Write a C program at `/home/user/src/extractor.c`. This program must read the TSV format from standard input (stdin) or file, decode the hex `Payload` into a standard ASCII string, and perform tokenization.
2. **Tokenization & Normalization**: A "word" is defined strictly as a contiguous sequence of one or more alphabetic characters (`A-Z`, `a-z`). Numbers, punctuation, and spaces are treated as delimiters and are not part of any word. 
3. **Feature Extraction**: Count the number of valid words in the decoded payload.
4. Output the processed data in Comma-Separated Values (CSV) format with the columns: `Timestamp,SensorID,WordCount`. There should be no spaces after the commas. Do not include a header row.
5. Create a multi-stage orchestration using `make`. Write a `/home/user/src/Makefile`. It must have a default `all` target that compiles the C program, and a `run` target that executes the pipeline, reading `/home/user/data/raw_logs.tsv` and writing the final output strictly to `/home/user/output/features.csv`.

Ensure your C code handles memory safely and efficiently. Do not use any external libraries other than the standard C library.

Make sure to create the `/home/user/output` directory if it does not exist in your pipeline execution.