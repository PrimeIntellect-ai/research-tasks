You are a security engineer tasked with rotating credentials after discovering an intrusion. We found out that our old authentication system had a vulnerability: it accepted JSON Web Tokens (JWTs) with the algorithm set to `none` (`"alg": "none"`). 

We have isolated a log file containing recent JWTs used to access our system. Your task is to identify the compromised tokens, extract the affected user IDs, and generate new, secure tokens for those users.

You must complete this task by writing a Rust program.

Here are your instructions:
1. Parse the log file located at `/home/user/jwt_logs.txt`. Each line contains one JWT.
2. Decode the headers of these JWTs to find which ones used the `"alg": "none"` vulnerability. Note that JWT headers and payloads are Base64URL encoded.
3. For each vulnerable token, decode the payload and extract the value of the `"sub"` field (this is the user ID).
4. Generate a new, secure JWT for each extracted user ID. The new JWT must:
   - Use the `HS256` algorithm.
   - Have the header: `{"alg": "HS256", "typ": "JWT"}`
   - Have the payload: `{"sub": "<user_id>", "iat": 1700000000}` (ensure `iat` is an integer, not a string).
   - Be signed using the secret key: `SuperSecretKey2023`.
5. Write the newly generated tokens to a JSON file at `/home/user/rotated_tokens.json`. The JSON file should be a key-value map where the key is the user ID and the value is the new JWT string.

You may create a new Cargo project in `/home/user/jwt_rotator` to write and run your Rust code. You are allowed to use external crates (like `jsonwebtoken`, `base64`, `serde`, etc.) by adding them to your `Cargo.toml`.

Example of expected output format in `/home/user/rotated_tokens.json`:
```json
{
  "affected_user1": "eyJhbGci...",
  "affected_user2": "eyJhbGci..."
}
```