import uvicorn
import os
import sys
import socket

# Ensure the parent directory is in the path so we can import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def find_available_port(host: str, preferred_port: int, max_attempts: int = 20) -> int:
    for port in range(preferred_port, preferred_port + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                sock.bind((host, port))
                return port
            except OSError:
                continue
    raise RuntimeError(f"No free port found between {preferred_port} and {preferred_port + max_attempts - 1}")

if __name__ == "__main__":
    reload_enabled = os.getenv("FASTAPI_RELOAD", "").lower() in {"1", "true", "yes"}
    host = os.getenv("FASTAPI_HOST", "127.0.0.1")
    preferred_port = int(os.getenv("FASTAPI_PORT", "8000"))
    port = find_available_port(host, preferred_port)
    if port != preferred_port:
        print(f"Port {preferred_port} is busy, starting FastAPI on http://{host}:{port}/ instead.")
    else:
        print(f"Starting FastAPI on http://{host}:{port}/")
    uvicorn.run("main:app", host=host, port=port, reload=reload_enabled)
