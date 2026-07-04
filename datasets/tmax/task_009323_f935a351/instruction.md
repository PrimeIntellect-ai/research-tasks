You are a security engineer responsible for rotating credentials on an internal system. A local credential rotation service is running on `127.0.0.1` at port `9090`. We have an existing C++ client used to upload new SSH public keys to this service, but it was previously written by a rogue administrator who intentionally used a path traversal exploit to overwrite arbitrary system files and omitted proper authentication checks.

Your task is to securely rotate the SSH key by completing the following steps:

1. **Decrypt the New Key:** 
   You have been provided an encrypted SSH public key at `/home/user/new_key.pub.enc`. It was encrypted using `aes-256-cbc` with the password `SecureRotate2024!` and pbkdf2. Decrypt this file and save the output exactly to `/home/user/new_key.pub`.

2. **Fix the C++ Client:**
   There is a C++ source file at `/home/user/upload_client.cpp`. It currently constructs a raw HTTP POST request that exploits a path traversal vulnerability in the server (`../../../home/user/.ssh/authorized_keys`) and lacks the necessary authorization. 
   Modify the C++ code so that:
   - The path traversal is removed. The file parameter in the HTTP URI should be strictly `authorized_keys`.
   - An HTTP header `Cookie: auth=admin_rotate` is added to the request to pass the service's authentication layer.
   - The client reads the contents of the decrypted `/home/user/new_key.pub` and sends it as the HTTP request body. Ensure the `Content-Length` header is correctly calculated based on the file content.

3. **Execute the Rotation:**
   Compile your fixed client using `g++ -o /home/user/upload_client /home/user/upload_client.cpp`.
   Run the compiled client. If successful, the server will accept the key and safely store it in its internal secure directory.

Ensure the final correctly uploaded key resides on the server securely. You may use standard shell tools (like `openssl`) to handle the decryption step. Do not modify the server itself.