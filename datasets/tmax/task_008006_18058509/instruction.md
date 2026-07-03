You are a data scientist cleaning a search query log dataset before training an intent recognition model. The dataset contains multilingual queries, but it is noisy with inconsistent casing, punctuation, and duplicate searches by the same users.

Your task is to write and execute a C++ program that processes the log file and produces a cleaned, deduplicated, and sorted CSV file.

**Input Data:**
A pipe-separated text file located at `/home/user/queries.txt`.
Format: `Timestamp|UserID|Query`
(Note: Timestamps are in ISO 8601 format, e.g., `2023-10-01T10:00:00Z`).

**Processing Requirements:**
1. **Normalization:** 
   - Convert all ASCII uppercase letters (`A-Z`) in the `Query` field to lowercase.
   - Remove all ASCII punctuation characters from the `Query` field. Specifically, remove any character where the C standard library function `ispunct()` (in the "C" locale) would return true.
   - **Crucial:** The dataset contains UTF-8 multi-byte characters (e.g., emojis, accents, non-Latin scripts). You must process the text carefully to ensure that non-ASCII bytes are left completely intact and uncorrupted.
   - Do not remove spaces.
2. **Deduplication:**
   - Group the records by `UserID`.
   - If a user has searched for the exact same *normalized* query multiple times, keep only the record with the *earliest* (lexicographically smallest) `Timestamp`.
3. **Sorting:**
   - Sort the final deduplicated records first by `UserID` (ascending, lexicographically), and then by `Timestamp` (ascending, lexicographically).
4. **Output:**
   - Save the result to `/home/user/cleaned_queries.csv`.
   - The output must be a CSV file with the format: `UserID,Timestamp,NormalizedQuery`.
   - Do not include a header row in the output.

**Constraints:**
- Write your solution in C++ (e.g., `clean.cpp`).
- Compile and run it in your terminal. You may use `-std=c++17` or `-std=c++20`.
- Only standard C++ libraries are allowed (no Boost, ICU, etc.).

When you are finished, ensure `/home/user/cleaned_queries.csv` exists and matches the exact specifications.