You are acting as a compliance analyst tasked with generating secure audit trails for our logging infrastructure. We have a microservice architecture that handles security logs, located in `/app/`. 

The system consists of three services started by `/app/startup.sh`:
1. **Ingester** (`/app/ingester.py`): Receives external log events on HTTP port 5000.
2. **Validator** (`/app/validator.py`): Validates requests on HTTP port 5001 and passes them to storage.
3. **Storage** (`/app/storage.py`): Saves logs on HTTP port 5002.

Your task is to secure and fix this pipeline to meet compliance requirements:

**1. Network Security Policy:**
The Validator (port 5001) and Storage (port 5002) services are currently binding to `0.0.0.0`, exposing them to the entire network. Modify their source code so they only bind to localhost (`127.0.0.1`). The Ingester must remain accessible on `0.0.0.0:5000`.

**2. Audit Seed Extraction (Log Parsing):**
A legacy seed is required to sign audit logs, but it was lost. Parse the security log file at `/app/logs/security.log`. Find the event with `EventID=4421` and `Status=AuditMode`. Extract the `AuditKey` value, which is base64-encoded, and decode it to get the plaintext seed.

**3. Token Generation (Reverse Engineering & Cryptography):**
There is an obfuscated script at `/app/legacy_hasher.py`. Reverse engineer its logic to understand how the `X-Audit-Token` is generated using a seed and a payload.

**4. Ingester Integration:**
Modify `/app/ingester.py` so that whenever it receives an HTTP POST request at `/ingest` with a JSON payload, it calculates the correct `X-Audit-Token` using the plaintext seed you extracted, and includes this token in the headers when it forwards the request to the Validator service.

Once you have made the necessary modifications, start the services by running `/app/startup.sh &` and ensure the pipeline works end-to-end. The automated test will send a JSON payload to the Ingester and expect a 200 OK response indicating successful storage.