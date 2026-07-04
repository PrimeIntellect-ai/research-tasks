You are an AI assistant helping a data science researcher organize and clean tabular datasets. 

We have a pipeline that processes dataset metadata in CSV format. Recently, we've found that some datasets contain poisoned or corrupted entries in their "Description" column. We have isolated a few examples of clean dataset files and corrupted (evil) dataset files. 

Your task is to write a C++ program that acts as an automated filter to detect these corrupted datasets. 

**Environment Details:**
- **Clean Examples:** Located in `/home/user/data/clean/`
- **Corrupted Examples:** Located in `/home/user/data/evil/`
- **Legacy Embedding Model:** We have a stripped, compiled binary located at `/app/model_exec`. This is the proprietary embedding extractor we use for all our text. It takes a single string as a command-line argument and prints a 3-dimensional float vector to standard output (e.g., `0.123 0.456 0.789`). 

**Your Objective:**
1. Analyze the clean and evil CSV files. Extract the "Description" column from the rows.
2. Use the `/app/model_exec` binary to generate embeddings for these descriptions.
3. Discover the mathematical or statistical pattern in the resulting embeddings that distinguishes the clean datasets from the evil ones. (Hint: look at the dimensions of the output vectors).
4. Write a C++ program named `/home/user/filter.cpp` and compile it to the executable `/home/user/filter`.

**Requirements for `/home/user/filter`:**
- It must take a single command-line argument: the path to a CSV file.
- It must read the CSV file, extract the "Description" column (ignoring the header), and pass each description to `/app/model_exec`.
- If the file is deemed "clean" based on your discovered embedding pattern, the program must exit with status code `0`.
- If the file is deemed "evil" (contains one or more corrupted descriptions), the program must exit with status code `1`.
- Standard libraries only. You may use standard C++ system calls (like `popen`) to invoke the binary.

You must build the executable `/home/user/filter` so our automated pipeline can test it against a hidden evaluation corpus of clean and evil CSV files.