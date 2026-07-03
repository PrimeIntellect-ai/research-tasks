You are an artifact manager tasked with curating a binary repository. An old repository snapshot has been recovered, but its index is custom-compressed and encrypted. The parameters required to unlock it are stored in a scanned manifest image. 

Your workflow is as follows:

1. **Extract Decryption Parameters**:
   There is an image file located at `/app/manifest.png`. Use OCR tools (e.g., `tesseract`) to extract the text from this image. You will find a `DECRYPTION_KEY` (an integer) in the text.

2. **Decompress and Decrypt the Repository Index**:
   The repository index is located at `/app/repository/blob.bin`. It was encoded using the following custom process:
   - First, the raw text (a CSV file) was Run-Length Encoded (RLE). The RLE format consists of pairs of bytes: the first byte is the count (number of repetitions), and the second byte is the ASCII character.
   - Second, every byte of the resulting RLE binary was XOR'd with the `DECRYPTION_KEY` extracted from the manifest.
   
   Write a Go program that reads `/app/repository/blob.bin` via standard input, reverses the XOR encryption using the extracted key, decodes the RLE data, and outputs the raw CSV text to standard output.

3. **Transform the Data**:
   The decoded CSV will have the header `id,name,size`. 
   Filter the records to only include artifacts where the `size` is strictly less than 1000. 
   Transform these filtered records into a JSON array of objects.

4. **Serve the Data**:
   Write and start a Go HTTP server listening exactly on `127.0.0.1:8080`.
   The server must expose a single endpoint: `GET /artifacts`.
   This endpoint must return the transformed JSON data with the `Content-Type: application/json` header.
   The JSON format should look exactly like this:
   ```json
   {
     "artifacts": [
       {"id": "1", "name": "alpha.tar.gz", "size": 500},
       ...
     ]
   }
   ```

Keep the HTTP server running in the background so it can be verified. You may use shell commands and standard stream redirections to tie the steps together.