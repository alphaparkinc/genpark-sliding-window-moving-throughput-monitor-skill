import sys
import json
from client import ThroughputMonitor

monitor = ThroughputMonitor()

def handle_request(req):
    method = req.get("method")
    req_id = req.get("id")
    
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-sliding-window-moving-throughput-monitor-skill", "version": "1.0.0"}
            }
        }
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "record_token_arrival",
                        "description": "Records timestamp of generated token",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "timestamp": {"type": "number"}
                            }
                        }
                    },
                    {
                        "name": "get_telemetry_stats",
                        "description": "Calculates real-time TPS, TTFT, and inter-token latency percentiles",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "window_seconds": {"type": "number", "default": 10.0}
                            }
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        params = req.get("params", {})
        name = params.get("name")
        args = params.get("arguments", {})
        
        if name == "record_token_arrival":
            monitor.record_token(args.get("timestamp"))
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": "Token recorded"}]}}
        elif name == "get_telemetry_stats":
            stats = monitor.get_window_stats(args.get("window_seconds", 10.0))
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(stats, indent=2)}]}}
            
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def run():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "error": {"code": -32000, "message": str(e)}}) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    run()
