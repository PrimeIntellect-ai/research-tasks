You are a localization engineer tasked with building a text processing pipeline in Go. 

First, you must retrieve a secret replacement token from an audio file. An audio file is provided at `/app/instructions.wav`. Transcribe the spoken word in this audio file (it contains a single English word). This word is your `SECRET_TOKEN`.

Second, you have a CSV file at `/home/user/terms.csv` with two columns: `source` and `target`. You need to create an SQLite database at `/home/user/translations.db`, create a table named `dict` with columns `source` (TEXT) and `target` (TEXT), and bulk import the CSV data into this table.

Finally, write a Go program at `/home/user/process.go` and compile it to an executable at `/home/user/process`.
Your Go program must do the following:
1. Read input text from `stdin` until EOF.
2. Process the text line by line.
3. For each line, normalize the string to Unicode NFC.
4. Tokenize the line into words. For this task, a "word" is defined strictly as a sequence of English letters (A-Z, a-z). Punctuation, spaces, and numbers are not part of a word and must be preserved exactly as they are in the output.
5. For each word, check if it matches a `source` entry in the `translations.db` (case-sensitive). If it does, replace it with the corresponding `target` string.
6. If the word is exactly the literal string `SECRET`, replace it with the `SECRET_TOKEN` you transcribed from the audio file.
7. Print the resulting line to `stdout` (ensure exact newline preservation).

Requirements:
- Your final executable must be located at `/home/user/process`.
- The program must connect to `/home/user/translations.db` (or load it entirely into memory at startup for performance, as it will be tested with many inputs).
- It must perfectly preserve all non-letter characters (spaces, punctuation, emojis, etc.).
- Your program's output must be bit-exact equivalent to our reference implementation.

Please complete the setup and compile your program.