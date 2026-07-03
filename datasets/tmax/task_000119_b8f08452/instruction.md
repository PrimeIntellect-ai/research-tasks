You are a security engineer tasked with rotating credentials and replacing an insecure legacy authentication system. 

We are decommissioning a legacy binary validator (`/app/legacy_validator`) that handles password policy checks. Recently, we discovered that the original developer included backdoors in this binary. Furthermore, our monitoring indicates that old, compromised passwords are still being attempted by internal automated scripts, as seen in the system logs (`/app/auth_logs/auth.log`).

Your objective is to write a new, secure Bash-based password validator script at `/home/user/pass_filter.sh`. This script will be used to filter proposed new passwords.

To build the correct filtering rules, you must perform the following investigations:
1. **Audio Analysis:** The departed developer left a voicemail at `/app/voicemail.wav` containing DTMF tones that encode a numeric "emergency override PIN". You must decode this PIN (tools like `multimon-ng` or `sox` are available). Your filter must REJECT any password that starts with this PIN.
2. **Binary Analysis:** Reverse engineer or inspect `/app/legacy_validator` to find a hardcoded backdoor string (a string longer than 8 characters containing the substring "bckd"). Your filter must REJECT any password containing this exact backdoor string anywhere within it.
3. **Log Analysis:** Parse `/app/auth_logs/auth.log`. Extract all base64-encoded strings that appear after the keyword "FAILED_ATTEMPT: ". Decode these to find previously compromised passwords. Your filter must REJECT any password that exactly matches one of these compromised passwords.
4. **General Security:** Your filter must REJECT any password that is strictly less than 10 characters long.

**Implementation Details:**
Create your script at `/home/user/pass_filter.sh`. Ensure it is executable.
The script must take exactly one argument: the path to a text file containing a single proposed password.
- If the password violates ANY of the rules above (starts with the DTMF PIN, contains the ELF backdoor, matches an old log password, or is too short), the script must output `REJECT` to stdout and exit with code `1`.
- If the password passes all checks, the script must output `ACCEPT` to stdout and exit with code `0`.

**Testing:**
We have provided a set of test corpora:
- `/app/corpus/evil/`: Contains files with passwords that violate one or more of the rules.
- `/app/corpus/clean/`: Contains files with secure passwords that pass all rules.
You should test your script against these directories to ensure it behaves correctly. The automated verifier will call your script exactly as `/home/user/pass_filter.sh <file_path>` for each file in these corpora.