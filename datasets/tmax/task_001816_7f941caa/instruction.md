You are a compliance analyst tasked with generating an audit trail for a recent internal security assessment. 

You have been provided with an audio recording located at `/app/assessment_dictation.wav`. In this recording, a senior auditor dictates a series of legacy SSH ciphers and insecure TLS versions that were supposedly left enabled on a staging server during an authentication flow test. 

Your objective is to:
1. Process and transcribe the audio file to extract the exact list of dictated SSH ciphers and TLS versions.
2. Write a script (in Python, Ruby, or your preferred language) that tests local endpoints to verify if these specific configurations are active. The endpoints are:
   - SSH: `localhost:2222`
   - TLS: `localhost:8443`
3. Generate a compliance audit trail report at `/home/user/audit_trail.json` containing only the configurations from the audio that were successfully negotiated with the local endpoints. 

The JSON format must strictly be:
```json
{
  "active_ssh_ciphers": ["cipher1", "cipher2"],
  "active_tls_versions": ["TLSv1.0"]
}
```

You may install any standard transcription tools (like `whisper` via pip) or network testing tools (like `nmap`, `openssh-client`, `openssl`) necessary to complete this task.