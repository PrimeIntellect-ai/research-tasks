You are acting as a localization engineer managing a translation metrics ETL pipeline. Recently, the upstream extraction job experienced transient network failures, causing it to retry and produce duplicate translation records in our raw logs. 

Your task is to implement the "Transform" node of our DAG using C++ to deduplicate the data, extract efficiency features, and compute rolling mathematical statistics.

Here is the setup:
The raw data is located at `/home/user/data/raw_translations.csv`.
It has the following header: `Timestamp,JobId,StringId,TranslatorId,WordCount,DurationSeconds`

You need to write a C++ program at `/home/user/pipeline/transform.cpp` that does the following:
1. **Deduplication**: Parse the CSV. Records are uniquely identified by the combination of `JobId` and `StringId`. Because of the retries, there are duplicates. For any duplicate `JobId` + `StringId` pairs, keep ONLY the record with the highest (most recent) `Timestamp`. Discard the older ones.
2. **Feature Extraction**: For each valid deduplicated record, calculate the Words Per Minute (WPM).
   `WPM = WordCount / (DurationSeconds / 60.0)`
3. **Rolling Statistics**: Group the records by `TranslatorId`. For each translator, order their translation jobs by `Timestamp` in ascending order. Calculate a 3-record rolling average of the WPM. This means for a given record, the `RollingAvgWPM` is the average of the WPM of that record and the up to 2 immediately preceding records for that same translator.
4. **Output**: Write the processed data to `/home/user/data/rolling_stats.csv` with the header:
   `TranslatorId,Timestamp,JobId,StringId,WPM,RollingAvgWPM`
   The output must be sorted alphabetically by `TranslatorId`, and then chronologically by `Timestamp` (ascending). 
   Both `WPM` and `RollingAvgWPM` must be formatted to exactly 2 decimal places.

Additionally, create a shell script at `/home/user/pipeline/run_dag.sh` that compiles the C++ program (using `g++ -std=c++17 -O2`) into an executable named `transform` in the same directory, and then executes it.

Make sure the output file matches the expected format precisely.