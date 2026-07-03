apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/evidence
    cat << 'EOF' > /home/user/evidence/server_logs.tsv
Timestamp	Source IP	HTTP Method	Request URI	User-Agent	Cookie	Content-Security-Policy
2023-10-01T10:00:00Z	192.168.1.10	GET	/index.html	Mozilla/5.0 (Windows NT 10.0)	session=abc123	default-src 'self'
2023-10-01T10:01:00Z	10.0.0.5	GET	/admin	Mozilla/5.0 (compatible; X-Exfil-Agent/1.0)	session=0BAeDBoRA1wUBAoRSTtUVUNBHgUaUVI=	script-src 'self' 'unsafe-eval'
2023-10-01T10:02:00Z	10.0.0.5	POST	/api/data	Mozilla/5.0 (compatible; X-Exfil-Agent/1.0)	session=0BAeDBoRA1wUBAoRSTtUVUNBHgUaUlI=	default-src 'self'
2023-10-01T10:03:00Z	192.168.1.11	GET	/login	Mozilla/5.0 (Macintosh)	session=def456	script-src 'unsafe-inline'
2023-10-01T10:04:00Z	172.16.0.4	GET	/profile	Mozilla/5.0 (X11; Linux x86_64)	session=xyz789	default-src 'self'; script-src 'unsafe-eval'
EOF

    chmod -R 777 /home/user