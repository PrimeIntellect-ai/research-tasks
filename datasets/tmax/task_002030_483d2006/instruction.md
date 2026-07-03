As a storage administrator, you are tasked with recovering and deduplicating legacy storage archives. The previous administrator left a custom binary archive format and an audio voicemail explaining how to extract data from it.

First, transcribe or listen to the voicemail located at `/app/voicemail.wav`. It contains crucial instructions regarding:
1. The exact byte offset where the text payload begins in our `.dat` archive files.
2. The specific legacy character encoding used for the text payload.
3. A specific text replacement macro/rule that must be applied to the extracted text to clean up legacy system warnings.

Your task is to write a Python CLI script at `/home/user/archive_extractor.py`. 
The script must accept exactly one command-line argument: the path to a `.dat` archive file.

For the given file, your script must:
1. Open the file and extract the binary payload starting precisely at the byte offset mentioned in the voicemail, reading until the end of the file.
2. Decode the extracted bytes into a string using the character encoding specified in the voicemail.
3. Apply the exact text replacement rule mentioned in the voicemail to the decoded string.
4. Print the final cleaned string to standard output (without any extra logging or newline characters not present in the processed payload).

Ensure your script handles standard errors gracefully but primarily focuses on producing the exact bit-for-bit output expected. A verification suite will test your script by fuzzing it with hundreds of randomly generated archive files and comparing its standard output against a hidden reference oracle.