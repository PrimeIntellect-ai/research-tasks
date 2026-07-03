apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest

    mkdir -p /home/user

    cat << 'EOF' > /home/user/auth_logs.log
{"timestamp": "2023-10-24T10:00:00Z", "username": "guest", "status": "failed", "reason": "Invalid_Password"}
{"timestamp": "2023-10-24T10:05:00Z", "username": "sysadmin", "status": "blocked", "reason": "SQLi_Attempt", "input": "' OR 1=1 --"}
{"timestamp": "2023-10-24T10:10:00Z", "username": "operator", "status": "failed", "reason": "Invalid_Password"}
EOF

    cat << 'EOF' > /home/user/threat_intel.json
[
  {"id": 1, "payload": "' OR 1=1 --"},
  {"id": 2, "payload": "' OR 'a'='a"},
  {"id": 3, "payload": "admin' --"},
  {"id": 4, "payload": "' || 1=1 #"},
  {"id": 5, "payload": "'; DROP TABLE users; --"}
]
EOF

    cat << 'EOF' > /home/user/waf_regex.txt
(?i)(\bOR\b|\bAND\b|DROP|SELECT|UNION|'a'='a')
EOF

    echo -n "RedTeamEvasionSalt2024!" > /home/user/salt.key

    cat << 'EOF' > /home/user/.expected_evasion_payload.txt
sysadmin|' || 1=1 #|86b1b46a3b2b8e39ad85de51315995cfd59517e476fbaf2b28c5a17dece30c00
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user