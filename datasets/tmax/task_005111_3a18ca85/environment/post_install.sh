apt-get update && apt-get install -y python3 python3-pip jq coreutils
pip3 install pytest

useradd -m -s /bin/bash user || true
mkdir -p /home/user/app

cat << 'EOF' > /home/user/app/index.html
<!DOCTYPE html>
<html>
<head>
    <title>Basic App</title>
</head>
<body>
    <h1>Welcome</h1>
</body>
</html>
EOF

cat << 'EOF' > /home/user/app/server.js
const express = require('express');
const app = express();
const config = require('./config.json');

app.use((req, res, next) => {
    res.setHeader('Content-Security-Policy', config['Content-Security-Policy']);
    next();
});

app.get('/', (req, res) => {
    // Vulnerable to Reflected XSS (CWE-79)
    const name = req.query.name || 'Guest';
    res.send('<html><body><h1>Hello ' + name + '</h1></body></html>');
});

app.listen(3000);
EOF

cat << 'EOF' > /home/user/app/config.json
{
  "Content-Security-Policy": "default-src * 'unsafe-inline' 'unsafe-eval'"
}
EOF

cd /home/user/app
sha256sum index.html > /home/user/manifest.txt
sha256sum config.json >> /home/user/manifest.txt
# Fake hash for server.js to represent original state
echo "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  server.js" >> /home/user/manifest.txt

cd /

chmod -R 777 /home/user