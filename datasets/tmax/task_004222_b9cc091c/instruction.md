You are acting as an artifact manager responsible for curating legacy binary repositories. We need to process a large backlog of archived artifacts, but they were encoded using a custom, proprietary obfuscation/compression scheme created by a former engineer. 

The original source code for the tool is lost, but we found a scanned copy of the engineer's design notes in an image file located at `/app/obfuscation_rules.png`. 

Your task is to:
1. Read the image at `/app/obfuscation_rules.png` to understand the custom byte-level obfuscation algorithm.
2. Write a Python 3 script at `/home/user/obfuscator.py` that implements this exact algorithm.
    * The script MUST read raw binary data from standard input (`stdin`) and write the processed raw binary data to standard output (`stdout`). 
    * It must act as a standard pipe filter, correctly handling arbitrary binary streams (not just text).
3. Make the script executable.
4. Create a directory `/home/user/bin` and create a **symbolic link** named `/home/user/bin/obfuscate_stream` that points to your `/home/user/obfuscator.py` script.

Automated systems will test your symbolic link by piping thousands of random binary files through it and verifying that the output matches the expected bit-exact legacy format.