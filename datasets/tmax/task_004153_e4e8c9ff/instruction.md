You are a data scientist cleaning up and analyzing user feedback logs from two consecutive days. 

You have been provided with two files containing user feedback, but they were exported from different systems and are in different formats:
1. `/home/user/day1.csv` - A CSV file. The text you need is in the `feedback` column.
2. `/home/user/day2.json` - A JSON file containing an array of objects. The text you need is in the `comment` field.

Your task is to identify "emerging anomalies" in the feedback—specifically, new terms that suddenly spiked in usage on Day 2.

Perform the following steps:
1. Read the text fields from both files.
2. Tokenize and normalize the text: 
   - Convert all text to lowercase.
   - Extract words consisting only of alphanumeric characters (e.g., using a regex like `[a-z0-9]+`). 
   - Ignore any punctuation or special characters.
3. Group and count the word frequencies for Day 1 and Day 2 separately.
4. Detect anomalies: Find all words that appear exactly `0` times in Day 1, but appear `5` or more times in Day 2.
5. Sort these anomalous words alphabetically.
6. Write the sorted words to `/home/user/emerging_terms.txt`, with one word per line.

You may use any programming language (Python, bash, etc.) to complete this task.