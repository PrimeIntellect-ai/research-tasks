You are an engineer tasked with porting a Web Application Firewall (WAF) query normalizer to work in a minimal Linux container. The original C project fails to cross-compile due to linking errors with obscure web libraries, and we need a lightweight Python alternative anyway.

Your task is to write a Python script at `/home/user/normalize.py` that precisely mimics the behavior of the old normalizer. 

Here are the requirements for `/home/user/normalize.py`:
1. It must accept exactly one command-line argument: a raw URI query string (e.g., `user=admin&b=3+4&a=2*5`).
2. It must parse the key-value pairs separated by `&`.
3. For each value, it must evaluate basic mathematical expressions (only containing integers, `+`, `-`, and `*`). For example, `3+4` becomes `7`.
4. It must sort the resulting key-value pairs alphabetically by the key.
5. It must format the output as a single string joined by `|`, prefixed by a specific secret WAF salt. 
   Format: `<SALT>:<key1>=<val1>|<key2>=<val2>|...`
   Example: `RED_42:a=10|b=7|user=admin`

To find the correct `<SALT>` prefix, you must analyze the video file provided at `/app/network_status.mp4`. This video is a diagnostic recording consisting of 100 frames. Several frames in this video are entirely solid red (RGB: 255, 0, 0). The salt prefix is `RED_X`, where `X` is the exact count of completely red frames in the video.

Ensure your Python script is executable and prints *only* the final formatted string to standard output. Do not print any debugging information. The script must perfectly handle arbitrary keys (composed of alphanumeric characters) and valid arithmetic expressions in the values.