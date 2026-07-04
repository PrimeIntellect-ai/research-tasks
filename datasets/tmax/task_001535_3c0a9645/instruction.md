You are tasked with fixing an issue with our configuration management ETL pipeline. The pipeline frequently retries jobs, which has resulted in a large file containing duplicate configuration change events. 

Your objective is to write a C++ program that streams this large configuration log, normalizes the configuration keys, removes duplicates, and logs the pipeline statistics.

1. Write a C++ program named `/home/user/dedup_config.cpp`.
2. The program must read a CSV formatted input from standard input (`stdin`). The CSV has no header and contains three columns: `timestamp,config_key,config_value`.
3. The program must process the file line by line (streaming) so it can handle files larger than available memory.
4. **Normalization**: For each line, normalize the `config_key` by converting all letters to lowercase and replacing every non-alphanumeric character (anything other than `a-z` and `0-9`) with a single underscore `_`.
5. **Deduplication**: Keep track of the `timestamp` and the *normalized* `config_key`. If you encounter a line with a `timestamp` and *normalized* `config_key` that you have already seen, drop the line (it's a duplicate from an ETL retry).
6. Output the cleaned, normalized records to standard output (`stdout`) in the same format: `timestamp,normalized_config_key,config_value`.
7. Output pipeline monitoring statistics to standard error (`stderr`) EXACTLY in this format on a single line:
   `Processed: <N> lines, Duplicates dropped: <M> lines`
   (where `<N>` is the total number of lines read, and `<M>` is the number of duplicates dropped).

Compile your C++ program using `g++ -O2 /home/user/dedup_config.cpp -o /home/user/dedup_config`.

The input file is located at `/home/user/config_changes.csv`.
Run your program so that it takes `/home/user/config_changes.csv` as input, writes the standard output to `/home/user/cleaned_configs.csv`, and writes the standard error to `/home/user/pipeline.log`.