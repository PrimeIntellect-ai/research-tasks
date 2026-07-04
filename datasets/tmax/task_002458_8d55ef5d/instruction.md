You are a backup operator testing a restored email routing service. As part of the disaster recovery procedures, you need to recreate the filtering logic of the routing service in a fast Rust utility.

You have recovered a stripped, interactive binary of the original validation daemon at `/app/validator`. The binary expects interactive terminal input: it prompts `Enter route: `, to which you can feed an email routing string. It will respond with `[OK]` or `[REJECTED]` based on its internal secret rules.

Your task is to write a Rust program at `/home/user/classifier.rs` and compile it to `/home/user/classifier`.
Your compiled program must take a single file path as a command-line argument. The file will contain exactly one email routing string.
Your program must:
1. Print "VALID" and exit with code 0 if the string satisfies the rules of the `/app/validator`.
2. Print "INVALID" and exit with code 1 if the string is rejected by the `/app/validator`.

You can probe the `/app/validator` binary (using shell scripts, `expect`, or manual interaction) to reverse-engineer its validation logic before writing your Rust program. 

Requirements:
- Ensure your compiled binary is located exactly at `/home/user/classifier`.
- Your Rust tool must run completely offline and independently (it must NOT simply call `/app/validator` under the hood, as the automated test environment will not have `/app/validator` available).
- The solution will be evaluated against a hidden corpus of valid (clean) and invalid (evil) routing strings.