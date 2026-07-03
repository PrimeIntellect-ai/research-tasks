I'm organizing some old project files and need a custom archive scanning tool. I have a screenshot of our archiving rule configuration located at `/app/rule.png`. 

Please write a Go program that does the following:
1. Takes exactly one command-line argument: a path to a directory.
2. Recursively traverses that directory.
3. Finds all files that have the exact extension specified in the `EXTENSION` field from the image.
4. Treats each matching file as a `gzip` compressed stream.
5. Decompresses the stream in memory (do not write the uncompressed data to disk).
6. Counts the total number of lines across all these uncompressed streams that contain the exact string specified in the `KEYWORD` field from the image (case-sensitive matching).
7. Prints only the final integer count to standard output (followed by a newline).

Read the image to determine the exact extension and keyword to look for (you can use `tesseract` which is available on the system). 

Save your Go source code anywhere, but compile the final executable to exactly this path:
`/home/user/archive_scanner`

Ensure your program handles missing or unreadable files gracefully by skipping them, but valid gzip files matching the extension must be processed.