You are a red-team operator trying to craft an evasion payload for a highly restrictive target environment. We have intercepted an audio note from the target's system administrator at `/app/intercepted_comms.wav`.

Your mission consists of the following steps:

1. **Audio Analysis & Password Recovery**: Analyze `/app/intercepted_comms.wav` to recover the spoken password. You may use any Python libraries or tools available in your environment (e.g., `SpeechRecognition`, `pocketsphinx`, or `whisper` if installed, or you can write a short script to process it).
2. **Access Control Bypass**: Use the recovered password to extract the encrypted archive located at `/app/vault.zip`. Extract its contents to `/home/user/`.
3. **Binary Analysis**: Inside the archive is a proprietary binary named `fw_policy_oracle`. Ensure it has the correct file permissions to be executed. This binary takes a single command-line argument consisting of a semicolon-separated list of IP:PORT pairs (e.g., `10.0.0.5:80;192.168.1.1:8080`) and generates a specific set of firewall rules.
4. **Evasion Payload Generation**: The target environment blocks unknown ELF binaries, so we cannot drop `fw_policy_oracle` directly. You must reverse-engineer the logic of the oracle by probing it with different inputs.
5. Write a completely standalone Python script at `/home/user/evasion_payload.py` that takes the exact same command-line argument and produces the **exact same standard output** as the oracle for any valid input string. 

Constraints:
- Your payload must be written in Python 3.
- It must accept the input string as `sys.argv[1]`.
- The output must be bit-exact equivalent to the oracle's output (including newlines).

The automated verifier will randomly fuzz both your `/home/user/evasion_payload.py` script and the original binary with hundreds of combinations to ensure 100% behavioral equivalence.