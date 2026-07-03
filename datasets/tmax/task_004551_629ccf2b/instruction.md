You are a data scientist working on an NLP pipeline. You have received a raw dataset of user reviews in a CSV format, and you need to build a fast C++ data processing tool to clean the text, extract features, compute rolling statistics, and output the data in JSON Lines format while maintaining an execution log.

Create a C++ program at `/home/user/processor.cpp`, compile it, and run it to process the input dataset. 

**Input Data:**
File: `/home/user/raw_reviews.csv`
Format: CSV with columns `timestamp,user_id,review_text`

**Processing Rules:**
1. **Cleaning & Normalization:** For the `review_text` column, convert all characters to lowercase. Remove all characters except lowercase letters (a-z), digits (0-9), and spaces. Replace multiple consecutive spaces with a single space, and strip leading/trailing spaces.
2. **Deduplication:** Ignore any row where the `user_id` is exactly the same as the `user_id` of the *immediately preceding valid (non-skipped) row*.
3. **Feature Extraction:** Compute the `word_count` of the cleaned text. Words are separated by a single space. If the cleaned text is empty, the word count is 0.
4. **Rolling Statistics:** Maintain a rolling average of the `word_count` for the last 3 valid rows processed (inclusive of the current row). For the first row, it's just its own word count. For the second, the average of the first two, etc. Calculate this as a floating-point number.

**Output Data:**
File: `/home/user/clean_features.jsonl`
Format: JSON Lines (one valid JSON object per line).
Fields required for each processed valid row:
* `"user_id"`: (string)
* `"clean_text"`: (string)
* `"word_count"`: (integer)
* `"rolling_avg_3"`: (float, exactly formatted to 2 decimal places, e.g., `4.50`)

**Pipeline Logging:**
File: `/home/user/pipeline.log`
The program must write exactly one line to this log file at the end of execution:
`[INFO] Processed <X> valid records. Skipped <Y> duplicate records.`
(Where `<X>` and `<Y>` are the respective integer counts).

You may use standard C++ libraries (e.g., `<iostream>`, `<fstream>`, `<sstream>`, `<string>`, `<vector>`, `<iomanip>`, etc.). No external dependencies (like nlohmann/json) are provided, so you should construct the simple JSON strings manually. Compile your code with standard `g++`.