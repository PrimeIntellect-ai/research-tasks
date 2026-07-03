I am a log analyst investigating patterns in a system's application logs. The logs are located at `/home/user/logs/app.jsonl` in JSON-lines format. Our downstream systems are breaking because the `message` field in these logs contains various unicode escape sequences (like `\u0020`, `\u00A0`, `\u201C`) that our legacy parser can't handle. 

I need you to build a Bash pipeline to extract, normalize, tokenize, and sample these logs, and then schedule it to run automatically.

Perform the following tasks:
1. Create an executable Bash script at `/home/user/analyze.sh`.
2. The script must read `/home/user/logs/app.jsonl`.
3. Extract the `message` string from each JSON object.
4. Normalize and tokenize the text:
   - Decode standard unicode escape sequences into their actual characters (Hint: `jq -r` handles valid JSON unicode escapes automatically).
   - Tokenize the decoded text into individual words. A "word" here is strictly defined as a contiguous sequence of alphabetic characters (A-Z, a-z). Ignore all numbers, punctuation, and symbols.
   - Convert all extracted words to lowercase.
5. Perform systematic sampling on the continuous stream of tokens: extract exactly every 3rd word (i.e., the 3rd, 6th, 9th, 12th word, etc., across the entire file's combined token stream).
6. Write these sampled words, one per line, to `/home/user/logs/sampled_tokens.txt`.
7. Run the script manually once so `/home/user/logs/sampled_tokens.txt` is populated.
8. Set up a cron job for the current user (`user`) that schedules `/home/user/analyze.sh` to run every minute (`* * * * *`).

Ensure all files and directories have appropriate permissions so the script can execute without `sudo`.