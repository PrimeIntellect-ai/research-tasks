You are an AI assistant helping a machine learning researcher organize a newly acquired dataset. 

The researcher received an obfuscated dataset archive at `/app/raw_dataset.zip` and an image file at `/app/obfuscation_key.png`. 
The archive is known to contain some improperly constructed paths that attempt to write outside the extraction directory (a "Zip Slip" vulnerability) and could overwrite system files or `/home/user/important_notes.txt`. 

Your task is to:
1. Extract the integer obfuscation key from `/app/obfuscation_key.png` (you may use `tesseract` for OCR). The image contains text in the format `KEY=XXX`.
2. Write a Python script to securely extract the contents of `/app/raw_dataset.zip` into `/home/user/clean_dataset/`. Your script MUST ignore/discard any files in the archive that attempt path traversal (e.g., paths containing `../` or absolute paths outside the target directory).
3. The valid files inside the archive are JPEG images that have been obfuscated. For every safely extracted file, you must apply a bitwise XOR operation to every byte of the file using the integer KEY extracted from the image.
4. Finally, bulk rename the successfully decoded images in the `/home/user/clean_dataset/` directory to follow a sequential naming pattern: `dataset_001.jpg`, `dataset_002.jpg`, etc. The assignment of numbers must be based on the alphabetical order of their original filenames in the ZIP archive.

Make sure the final images are valid JPEGs. An automated test will evaluate the Mean Squared Error (MSE) between your `dataset_001.jpg` and a hidden reference image to ensure proper extraction and decoding.