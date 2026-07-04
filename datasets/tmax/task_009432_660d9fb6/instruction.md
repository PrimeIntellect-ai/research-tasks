You are a log analyst investigating a highly sophisticated spam and astroturfing campaign on a multi-lingual chat server. The attackers are using bots to post slightly modified messages across different accounts within short time frames. To bypass simple filters, they use Unicode variations and minor typos.

Your task is to write a C program that processes a chat log file to detect these coordinated anomalous patterns.

The input log file is located at `/home/user/chat_logs.txt`.
Each line in the log file has the following format:
`[YYYY-MM-DDTHH:MM:SSZ] | [UserID] | [Message]`

For example:
`2023-10-01T12:00:00Z | U01 | Hello world!`
`2023-10-01T12:05:00Z | U05 | こんにちは`

Write a C program at `/home/user/detect_spam.c` and compile it to `/home/user/detect_spam`. The program must do the following:

1. **Timestamp Parsing & Rolling Window:** Iterate through the log chronologically. For each message, maintain a "rolling window" of all messages that occurred strictly within the last 60 seconds (i.e., `0 <= CurrentMessageTime - PreviousMessageTime <= 60`).
2. **Rolling Statistics:** For each message, calculate the `WindowMsgCount`, which is the total number of messages in the log that fall into its 60-second rolling window (including the current message itself).
3. **Multi-language Distance Computation:** For each new message, compare its message text to the text of every *previous* message currently in its 60-second window. Calculate the Levenshtein distance between the two messages based on **UTF-8 code points**, NOT bytes. 
4. **Suspicious Pattern Matching:** A pair of messages is flagged as suspicious if:
   - Their UTF-8 code point Levenshtein distance is `<= 2`.
   - The two messages were sent by *different* UserIDs.
5. **Output:** For every suspicious pair found, append a record to `/home/user/suspicious_patterns.csv` in the exact format:
   `CurrentTimestamp,PreviousUserID,CurrentUserID,Distance,WindowMsgCount`

*Notes:*
- The input logs are guaranteed to be in strict chronological order and valid UTF-8.
- If a current message matches multiple previous messages in the window, output a separate line for each match, in the order the previous messages appeared in the log.
- Do not use third-party libraries outside of the standard C library (e.g., `<stdio.h>`, `<stdlib.h>`, `<string.h>`, `<time.h>`). You must implement the UTF-8 parsing and Levenshtein algorithm yourself.
- Ensure your output file does not contain spaces after the commas.