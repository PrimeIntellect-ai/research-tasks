You are an AI assistant helping a data analyst process a corrupted ETL job dump. 

An ETL pipeline recently failed and retried multiple times, resulting in a CSV file (`/home/user/etl_dump.csv`) that contains duplicate records. Additionally, some text fields got corrupted with messy casing, and some numerical measurements were lost.

Your task is to write a C program (`/home/user/process_etl.c`) that processes this file line-by-line, resolves the duplicates, normalizes the data, imputes missing values, extracts new features, and outputs a clean CSV.

Here are the specific requirements for your C program:

1. **Input/Output Requirements**:
   - Read from `/home/user/etl_dump.csv`. The file has no header. The format is: `ID,Timestamp,Username,Measurement,Notes`.
   - Write to `/home/user/clean_data.csv`. The output format should be: `ID,Normalized_Username,Imputed_Measurement,Notes_Word_Count`.
   - You must stream the file line-by-line (e.g., using `fgets` or `getline`). Do not load the entire file into memory, as in a real scenario this file would be gigabytes in size.

2. **Deduplication (ETL Retry Handling)**:
   - The input file is pre-sorted by `ID`, but contains duplicate rows for the same `ID` due to ETL retries. 
   - You must keep only the **last** row for each unique `ID` (representing the final state of the retry).

3. **Tokenization and Normalization**:
   - The `Username` field has inconsistent casing and surrounding whitespace. 
   - You must trim all leading and trailing whitespace (spaces and tabs) and convert the entire username to lowercase.

4. **Interpolation/Imputation**:
   - The `Measurement` field is a float. Sometimes it is missing (represented as `NA` or an empty string).
   - If a measurement is missing, impute it by carrying forward the **last valid measurement seen in the entire file stream up to that point**. (If no valid measurement has been seen yet at the start of the file, use `0.0`). Format floats to 1 decimal place (e.g., `%.1f`).

5. **Feature Extraction & Encoding Handling**:
   - Extract a feature from the `Notes` field: the word count.
   - For this calculation, a "word" is defined as a contiguous sequence of strictly ASCII alphanumeric characters (A-Z, a-z, 0-9). 
   - The `Notes` field may contain UTF-8 or corrupted non-ASCII characters. You must completely ignore any non-ASCII bytes (bytes with the high bit set) and punctuation when counting words. For example, "café" would be treated as "caf" (1 word) if 'é' is non-ASCII.

**Execution**:
- Compile your program using `gcc /home/user/process_etl.c -o /home/user/process_etl`.
- Run your program. It should read `/home/user/etl_dump.csv` and generate `/home/user/clean_data.csv`.