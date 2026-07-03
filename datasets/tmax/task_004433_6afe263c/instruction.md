You are an AI assistant helping a data analyst process messy data feeds.

I have a large, continuous stream of messy CSV records that need to be normalized before they can be loaded into our data warehouse. The incoming data format always has exactly 3 columns. 

We received a scanned image of the legacy data normalization requirements. The image is located at `/app/transformation_rules.png`.

Your task is to:
1. Extract the text from the image to figure out the exact normalization rules for the three columns. (You may need to install an OCR tool like Tesseract).
2. Write a Go program that reads a stream of CSV data from `stdin` and writes the cleaned CSV data to `stdout`.
3. Your Go program must be designed for large-file streaming (process line-by-line or chunk-by-chunk; do not load the entire input into memory).
4. Apply the tokenization and normalization rules exactly as specified in the image.
5. Compile your Go program and place the executable at `/home/user/parser`.

Requirements for the Go program:
- Use the standard `encoding/csv` library.
- Read records of exactly 3 columns from `stdin`.
- If a CSV line is completely malformed, skip it.
- Apply the rules from the image to each column.
- Write the transformed 3-column record to `stdout` in standard CSV format.
- Ensure the output is flushed before the program exits.

You have full access to install any necessary tools via `apt-get` to read the image. Once you have built the executable at `/home/user/parser`, you are done. An automated verification suite will pipe large amounts of random CSV fuzz data into your program and compare its output bit-for-bit against our reference parser.