apt-get update && apt-get install -y python3 python3-pip nodejs npm redis-server curl
    pip3 install pytest redis

    useradd -m -s /bin/bash user || true
    mkdir -p /home/user/app
    cd /home/user/app

    npm install express redis uuid

    cat << 'EOF' > /home/user/app/oracle_worker
#!/usr/bin/env python3
import sys, base64

def eval_expr(expr):
    tokens = expr.replace('(', ' ( ').replace(')', ' ) ').split()
    def parse(tokens):
        if not tokens: raise SyntaxError("unexpected EOF")
        token = tokens.pop(0)
        if token == '(':
            L = []
            while tokens[0] != ')':
                L.append(parse(tokens))
            tokens.pop(0)
            return L
        else:
            try: return int(token)
            except ValueError: return token

    ast = parse(tokens)

    def evaluate(node):
        if isinstance(node, int): return node
        op = node[0]
        args = [evaluate(x) for x in node[1:]]
        if op == 'ADD': return args[0] + args[1]
        if op == 'SUB': return args[0] - args[1]
        if op == 'MUL': return args[0] * args[1]
        if op == 'DIV': return args[0] // args[1]
        raise ValueError("Unknown op")

    return evaluate(ast)

if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[1] == '--cli':
        expr = base64.b64decode(sys.argv[2]).decode('utf-8')
        print(eval_expr(expr))
EOF
    chmod +x /home/user/app/oracle_worker

    cat << 'EOF' > /home/user/app/gateway.js
const express = require('express');
const redis = require('redis');
const { v4: uuidv4 } = require('uuid');

const app = express();
app.use(express.json());

const REDIS_PORT = 6380;
const JOB_QUEUE = 'old_jobs';
const RESULT_QUEUE = 'math_results';

const client = redis.createClient({ url: `redis://127.0.0.1:${REDIS_PORT}` });
client.connect().catch(console.error);

app.post('/calc', async (req, res) => {
    const expr = req.body.expr;
    const id = uuidv4();
    const payload = Buffer.from(expr).toString('base64');

    await client.lPush(JOB_QUEUE, JSON.stringify({ id, payload }));

    const checkResult = async () => {
        const result = await client.rPop(RESULT_QUEUE);
        if (result) {
            const data = JSON.parse(result);
            if (data.id === id) {
                return res.json({ result: data.result });
            } else {
                await client.lPush(RESULT_QUEUE, result);
            }
        }
        setTimeout(checkResult, 100);
    };
    checkResult();
});

app.listen(8080, () => console.log('Gateway listening on port 8080'));
EOF

    cat << 'EOF' > /home/user/app/start.sh
#!/bin/bash
redis-server --daemonize yes
node /home/user/app/gateway.js &
python3 /home/user/app/worker.py &
wait
EOF
    chmod +x /home/user/app/start.sh

    chmod -R 777 /home/user