As a penetration tester, you have intercepted a proprietary encryption tool (`/home/user/custom_cryptor`) and an encrypted file containing sensitive information (`/home/user/stolen_data.enc`). 

Through preliminary analysis, you know the following:
1. The `custom_cryptor` is a 64-bit Linux ELF executable.
2. The developer made a fatal mistake: they hardcoded the static encryption key into a custom ELF section named `.keys`.
3. The encryption algorithm is a simple repeating-key XOR cipher. The key length is exactly 8 bytes.

Your objective is to:
1. Extract the 8-byte key from the `.keys` section of the `/home/user/custom_cryptor` ELF binary.
2. Write a Python script at `/home/user/decrypt.py` that reads this key and decrypts the contents of `/home/user/stolen_data.enc`.
3. Save the successfully decrypted plaintext to `/home/user/decrypted.txt`.

Your Python script must handle the extraction and decryption processes programmatically (you may use standard libraries or install modules like `pyelftools` via pip if needed). 

Ensure that `/home/user/decrypted.txt` contains only the exact decrypted string, with no additional formatting or padding.