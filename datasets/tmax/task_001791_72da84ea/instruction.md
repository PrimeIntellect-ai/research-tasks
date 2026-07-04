You are acting as a storage administrator managing disk space on a critical system. The application generates massive log files, and the log rotation process is racing with the writing process. To save disk space efficiently, the engineering team has defined a custom, high-speed Run-Length Encoding (RLE) compression algorithm specifically tuned for our log formats.

Your task is to implement this custom compressor. 

First, you need to retrieve the compression parameters. The previous administrator left them in an image file located at `/app/config.png`. You will need to extract the `ESCAPE` character and the `MIN_RUN` integer threshold from this image.

Next, implement the compressor program. You must create an executable file at `/home/user/compress_rotate` (you can use Python, Perl, Ruby, bash, or C/C++ compiled to this path). The program must read raw text from Standard Input (stdin) and write the compressed text to Standard Output (stdout).

The custom RLE compression rules are as follows:
1. Any consecutive sequence of the identical character with a length greater than or equal to `MIN_RUN` must be compressed into the following format: `[ESCAPE][character][length][ESCAPE]`. 
   For example, if `ESCAPE` is `~` and `MIN_RUN` is `4`, the string `baaaac` becomes `b~a4~c`. `aaaaaaaaaaaa` becomes `~a12~`.
2. Any literal appearance of the `ESCAPE` character in the input must be escaped by doubling it. 
   For example, `~` becomes `~~`.
3. If the `ESCAPE` character itself appears consecutively `MIN_RUN` or more times, it is compressed just like any other character, but using its escaped form. 
   For example, `~~~~` (4 times) becomes `~~4~`. 

Your program must exactly implement this logic, processing character by character. An automated verifier will aggressively test your `/home/user/compress_rotate` executable against a reference oracle by feeding it millions of randomly generated characters (including edge cases with long runs and lots of escape characters) to ensure bit-exact equivalence.

Ensure your program is executable (`chmod +x /home/user/compress_rotate`).