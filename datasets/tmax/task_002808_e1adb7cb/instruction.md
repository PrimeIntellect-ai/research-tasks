You are tasked with building a robust data cleaning pipeline script for an incoming stream of textual records. As a data scientist, you need to ensure the data is properly tokenized, cleaned, and transformed before it is stored in our large-scale data storage system. 

We have received a configuration image containing specific data cleaning parameters, located at `/app/config_image.png`. You must extract these parameters (which include a list of invalid tokens and a statistical threshold value) using OCR (Tesseract is available on the system).

Your objective is to write a Python script at `/home/user/etl_cleaner.py` that acts as a Unix filter. It should read lines of text from standard input (stdin) and write the processed lines to standard output (stdout). 

For each line of input text:
1. Tokenize the text by splitting on whitespace.
2. Remove any tokens that exactly match the invalid tokens listed in the image.
3. Compute the average length of the remaining tokens.
4. If the average length is greater than or equal to the statistical threshold value extracted from the image, output the joined remaining tokens (separated by a single space). Otherwise, output the string `REJECTED`.

Ensure your script handles empty inputs gracefully (outputting `REJECTED`). The script must be executable and start with the standard python3 shebang. We will test your script against thousands of random input records to ensure it exactly matches our strict internal reference implementation.