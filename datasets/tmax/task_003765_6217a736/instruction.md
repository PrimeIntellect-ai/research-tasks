I am a researcher organizing a large collection of custom dataset archives. I'm worried about security vulnerabilities like "zip slip" where malicious paths could overwrite system files, so I need to process these archives carefully.

I have an image of the processing and sanitization rules that my team agreed upon located at `/app/rules.png`. You will need to extract the text from this image (you can use `tesseract`) to understand the exact parsing and sanitization rules.

Your task is to write a robust Bash script at `/home/user/process_archive.sh` that reads our custom archive format from standard input (`stdin`) and writes the sanitized, processed output to standard output (`stdout`). 

The custom archive format is a text stream containing multiple files, structured as follows:
```
BEGIN FILE: <filepath>
<content line 1>
<content line 2>
...
END FILE
```

There can be multiple such blocks in the input stream. Lines outside of a `BEGIN FILE` and `END FILE` block should be ignored.

Please write the `/home/user/process_archive.sh` script (make it executable) so that it strictly adheres to the sanitization rules found in the image. The script must handle arbitrary text contents within the files and strictly follow the formatting requirements for the output. Do not include any extraneous output; your script's standard output will be aggressively tested against a reference implementation with randomized inputs.