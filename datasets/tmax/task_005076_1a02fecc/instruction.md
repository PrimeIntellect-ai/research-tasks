You are a QA engineer tasked with setting up a local mock environment for a proprietary telemetry ingestion system. The actual backend is unavailable, so you need to build a mock WebSocket server in Python to enable end-to-end test orchestration for the frontend teams.

The telemetry protocol requires the server to acknowledge received payloads by returning a proprietary checksum. The base of the checksum algorithm is standard CRC32, as shown in this legacy JavaScript snippet located at `/home/user/legacy_checksum.js` (which you will need to translate to Python):

```javascript
// /home/user/legacy_checksum.js
// Base CRC32 implementation
function makeCRCTable() {
    var c;
    var crcTable = [];
    for(var n =0; n < 256; n++){
        c = n;
        for(var k =0; k < 8; k++){
            c = ((c&1) ? (0xEDB88320 ^ (c >>> 1)) : (c >>> 1));
        }
        crcTable[n] = c;
    }
    return crcTable;
}

function get_base_checksum(str) {
    var crcTable = window.crcTable || (window.crcTable = makeCRCTable());
    var crc = 0 ^ (-1);
    for (var i = 0; i < str.length; i++ ) {
        crc = (crc >>> 8) ^ crcTable[(crc ^ str.charCodeAt(i)) & 0xFF];
    }
    return (crc ^ (-1)) >>> 0;
}
```

However, the final checksum calculation includes an additional proprietary bitwise mixing step that is not documented. To help you figure it out, the core team has provided a stripped Linux binary at `/app/telemetry_oracle`. This binary takes a base64-encoded string as a command-line argument and prints the final 8-character hex checksum (lowercase). 

Your tasks are:
1. Translate the base CRC32 logic to Python.
2. Reverse-engineer or deduce the missing proprietary mixing step by using `/app/telemetry_oracle` as a black-box oracle.
3. Write a property-based test in `/home/user/test_checksum.py` using the `hypothesis` library. This test must assert that your Python implementation produces the exact same output as the oracle for any arbitrary byte sequence.
4. Implement and run a Python WebSocket server using the `websockets` library.
   - The server must listen on `127.0.0.1:8765` at the path `/telemetry`.
   - It should accept JSON messages in the format: `{"id": <int>, "data": "<base64_encoded_string>"}`.
   - For each message, it must compute the proprietary checksum of the decoded data and reply with JSON: `{"id": <int>, "status": "ack", "checksum": "<8_char_hex_string>"}`.
5. Start the WebSocket server and leave it running in the background so that our automated test suite can connect to it.

Ensure all dependencies (like `websockets` and `hypothesis`) are installed in your Python environment.