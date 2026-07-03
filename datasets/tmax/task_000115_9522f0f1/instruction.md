You are an automation specialist tasked with creating a C-based data processing workflow to handle multi-lingual customer support logs.

We have two input files located in `/home/user/data/`:
1. `/home/user/data/profiles.csv`: A CSV file containing user profiles with headers `UserID,Name,Region`.
2. `/home/user/data/chats.txt`: A pipe-delimited text file containing unstructured chat logs with headers `LogID|Message`. The messages are multi-lingual (UTF-8) and contain embedded user references and sensitive email addresses.

Your objective is to write a C program (`/home/user/processor.c`) that performs the following operations:
1. **Extraction**: Parse each line of `chats.txt`. Extract the `LogID`. Extract the `UserID` from the message text, which always appears in the exact format `[USER:123]` (where `123` is the UserID).
2. **Data Masking**: Find any email addresses in the message and replace them with the exact string `[REDACTED]`. For this task, an email address is strictly defined by the POSIX Extended Regular Expression: `[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}`
3. **Join/Merge**: Look up the extracted `UserID` in the `profiles.csv` file to find the user's `Name` and `Region`. If a UserID is not found in the profiles, use `Unknown` for both Name and Region.
4. **Unicode Processing**: Calculate the length of the *masked* message in **characters** (not bytes). Since the text is UTF-8 encoded, you must correctly count multi-byte characters (e.g., using `mbstowcs` or similar with the correct locale).

Compile your program (e.g., `gcc -o /home/user/processor /home/user/processor.c`) and run it to produce an output file at `/home/user/results.csv`.

The output file `/home/user/results.csv` must be a valid CSV file with the following exact headers:
`LogID,UserID,Name,Region,MessageLength,MaskedMessage`

Rules and Constraints:
- Use only standard C libraries (e.g., `<stdio.h>`, `<stdlib.h>`, `<string.h>`, `<regex.h>`, `<locale.h>`, `<wchar.h>`).
- Do not use external libraries like PCRE; use the POSIX `<regex.h>` available in glibc.
- Ensure your program gracefully skips the header line of the input files.
- The `MessageLength` should be the number of characters (code points), not bytes, of the `MaskedMessage`.
- Double quotes inside the `MaskedMessage` in the CSV output are not required to be escaped for this specific task unless they break your basic CSV formatting. To keep it simple, assume the input text does not contain double quotes, commas, or newlines in the message body.