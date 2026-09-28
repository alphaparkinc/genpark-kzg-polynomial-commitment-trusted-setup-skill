import sys
import json
from client import KZGCommitment

kzg = KZGCommitment()

def handle_request(req):
    method = req.get("method")
    params = req.get("params", {})
    req_id = req.get("id")

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "kzg_commit_evaluate",
                        "description": "Commit to polynomial or evaluate at point under KZG SRS",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "action": {"type": "string", "enum": ["commit", "evaluate"]},
                                "poly_coeffs": {"type": "array", "items": {"type": "integer"}},
                                "z": {"type": "integer"}
                            },
                            "required": ["action", "poly_coeffs"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})
        if name == "kzg_commit_evaluate":
            act = args["action"]
            coeffs = args["poly_coeffs"]
            if act == "commit":
                c = kzg.commit(coeffs)
                return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps({"commitment": c})}]}}
            elif act == "evaluate":
                val = kzg.evaluate(coeffs, args.get("z", 0))
                return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps({"evaluation": val})}]}}
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        if line.strip():
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
