You are acting as a compliance analyst for our organization. We need to generate clean, compliance-ready audit trails from our raw unified security logs. 

Our senior security engineer left a voice memo detailing the exact filtering logic required for the new compliance standard, specifically focusing on SSH hardening rules and WAF injection/XSS log redaction.

Your tasks:
1. Locate the audio file at `/app/instructions.wav`. You will need to transcribe or listen to this file (e.g., using `whisper` or similar tools you can install) to understand the exact filtering rules.
2. Write a Python script at `/home/user/audit_generator.py` that processes a raw JSON log file and outputs a filtered JSON audit trail based on the rules dictated in the audio.
3. Your script must accept exactly two command-line arguments: the input file path and the output file path.
   Usage: `python3 /home/user/audit_generator.py <input_log.json> <output_trail.json>`

The input will be a JSON array of objects. Each object represents a log event.
The output must be a JSON array of the filtered objects, formatted with an indentation of 2 spaces (`indent=2` in Python's `json.dump`).

Your script's output must be BIT-EXACT equivalent to our internal reference oracle for all possible valid log inputs. The filtering logic strictly depends on the SSH key management rules and injection/XSS payload matching mentioned in the recording.