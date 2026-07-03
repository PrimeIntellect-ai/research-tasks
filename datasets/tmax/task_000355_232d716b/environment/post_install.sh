apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest networkx

    mkdir -p /home/user/data

    cat << 'EOF' > /home/user/data/routers.csv
router_id,properties
R1,"{""region"": ""US-East"", ""active"": true, ""capacity"": 100}"
R2,"{""region"": ""US-East"", ""active"": true, ""capacity"": 40}"
R3,"{""region"": ""US-West"", ""active"": true, ""capacity"": 200}"
R4,"{""region"": ""EU-West"", ""active"": false, ""capacity"": 500}"
R5,"{""region"": ""US-East"", ""active"": true, ""capacity"": 60}"
R6,"{""region"": ""US-West"", ""active"": true, ""capacity"": 150}"
R7,"{""region"": ""Asia"", ""active"": true, ""capacity"": 80}"
R8,"{""region"": ""US-East"", ""active"": true, ""capacity"": 90}"
R9,"{""region"": ""US-West"", ""active"": false, ""capacity"": 300}"
R10,"{""region"": ""US-East"", ""active"": true, ""capacity"": 55}"
R11,"{""region"": ""US-West"", ""active"": true, ""capacity"": 10}"
R12,"{""region"": ""US-East"", ""active"": true, ""capacity"": 70}"
R13,"{""region"": ""US-West"", ""active"": true, ""capacity"": 85}"
R14,"{""region"": ""US-East"", ""active"": true, ""capacity"": 95}"
R15,"{""region"": ""US-West"", ""active"": true, ""capacity"": 120}"
R1,{region: US-East, active: true, capacity: 100}
R15,{region: US-West, active: true, capacity: 120}
EOF

    cat << 'EOF' > /home/user/data/links.csv
source,target,latency_ms
R1,R2,10
R1,R5,20
R2,R3,15
R5,R3,25
R3,R6,10
R5,R6,40
R6,R7,5
R7,R8,10
R6,R8,20
R8,R10,15
R8,R4,5
R4,R15,10
R10,R12,5
R12,R13,10
R13,R15,15
R10,R15,40
R1,R14,50
R14,R15,20
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user