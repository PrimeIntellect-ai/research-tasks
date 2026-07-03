I am a researcher organizing a massive, old archive of text datasets for a new machine learning pipeline. I have a collection of raw text files in `/home/user/raw_data`, but they are a mess: they are in different encodings, have varying sizes, and are mixed with newer files that I don't want to include.

I need you to write a C++ program that automates the organization of these datasets based on a configuration file. 

Here are the requirements:

1. **Configuration Interpretation:**
   Read a configuration file located at `/home/user/pipeline.conf`. The file will be in a simple INI-like format:
   ```ini
   [Input]
   Directory=/home/user/raw_data
   Extension=.dat
   MaxYear=2021
   OriginalEncoding=WINDOWS-1252

   [Output]
   Directory=/home/user/processed_data
   Prefix=dataset_chunk_
   LinesPerChunk=50
   TargetEncoding=UTF-8
   ```

2. **Metadata-Based File Search:**
   Your C++ program must scan the `Directory` specified in `[Input]`. It should exclusively select files that:
   - End with the specified `Extension`.
   - Have a Last Modification Date less than or equal to December 31st of the `MaxYear`.

3. **Character Encoding Conversion & File Merging:**
   For all the valid files found (sorted alphabetically by filename to ensure deterministic merging), read their contents. The files are currently encoded in the `OriginalEncoding`. You must convert their contents to the `TargetEncoding` (UTF-8) in memory. You may use standard C/C++ libraries like `iconv` for this.

4. **File Splitting and Chunking:**
   Merge the decoded text from all valid files and split the output into multiple chunk files in the `[Output]` Directory.
   - Each chunk must contain exactly `LinesPerChunk` lines, except possibly the last chunk, which will contain the remainder.
   - The output files should be named using the `Prefix` followed by a 3-digit zero-padded index starting from 001 (e.g., `dataset_chunk_001.txt`, `dataset_chunk_002.txt`).

Please write the C++ program to `/home/user/dataset_organizer.cpp`. Write a `Makefile` or build script if necessary, compile the program, and execute it using the existing `/home/user/pipeline.conf` file. The final processed files must be correctly written to `/home/user/processed_data/`.