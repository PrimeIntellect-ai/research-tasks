You are acting as a data scientist cleaning a dataset of job titles. You have received a messy JSON-lines file where the system that generated it failed to properly escape unicode characters, leaving broken escape sequences in the text. 

Your task is to write a C++ program `/home/user/process_data.cpp` that performs a data cleaning and similarity scoring pipeline. 

Requirements for your C++ program:
1. **Read** the input file located at `/home/user/data/dirty_records.jsonl`. 
   Each line is a JSON object with this exact format: `{"id": <integer>, "text": "<string>"}`.
2. **Extract** the `id` and `text` values. You must use standard C++ regex to parse the line, as no external JSON libraries are guaranteed to be available.
3. **Clean** the `text` field using regex. The text contains malformed unicode escape sequences. You must remove any substring that matches the pattern: a literal backslash `\`, followed by a lowercase `u`, followed by between 0 and 4 (inclusive) hexadecimal digits (`0-9`, `a-f`, `A-F`). Replace these matched substrings with an empty string. 
   *(Note: The backslash in the JSON file is literal, meaning the file contains the characters `\`, `u`, etc. not actual unprintable characters).*
4. **Compute** the Levenshtein distance (edit distance) between the cleaned text and the target string `"data scientist"`. Use standard operations (insert, delete, substitute) with a cost of 1 for each. The distance calculation must be case-sensitive.
5. **Output** the results to `/home/user/output/distances.csv`. The file should contain a header row `id,distance`, followed by one row per record sorted by `id` in ascending order.

Once you have written the code, compile it using `g++ -std=c++17` and run it to produce the output file. 

Example of cleaning:
Original text: `data \u202scientist`
Cleaned text: `data scientist`
Distance to `"data scientist"`: 0