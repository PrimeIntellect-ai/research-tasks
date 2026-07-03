You are an AI assistant helping a data researcher process multiple datasets concurrently. 

The researcher has a basic C++ program `/home/user/writer.cpp` that appends metrics to `/home/user/results.csv`. However, when run concurrently, the output gets interleaved and corrupted because the program lacks file locking. 

Additionally, the researcher has a configuration file `/home/user/datasets.conf` containing the names of datasets to process. Some lines are comments (starting with `#`) or section headers (starting with `[`).

Your task:
1. Edit `/home/user/writer.cpp` to implement exclusive file locking using `flock()` from `<sys/file.h>` right after the file is opened, and unlock it before closing. 
2. Compile the fixed C++ program to `/home/user/writer`.
3. Use text transformation tools (like `awk`, `sed`, or `grep`) to read `/home/user/datasets.conf`, ignore empty lines, comments (`#`), and headers (`[`), and extract the dataset names.
4. For each valid dataset extracted from the config file, launch a background instance of the compiled `/home/user/writer` passing the dataset name as the first argument. 
5. Wait for all background processes to finish.

The final output must be a clean, uncorrupted `/home/user/results.csv` file containing the metrics for only the active datasets specified in the config. Each active dataset will result in exactly 20 lines written to the CSV.