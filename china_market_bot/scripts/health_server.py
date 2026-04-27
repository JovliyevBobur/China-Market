import http.server
import socketserver
import os
from loguru import logger

# Get port from environment or default to 8080
PORT = int(os.environ.get("PORT", 8080))

class HealthCheckHandler(http.server.SimpleHTTPRequestHandler):
    """Simple health check handler for Railway."""
    
    def do_GET(self):
        """Handle GET requests."""
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"OK")

    def log_message(self, format, *args):
        """Suppress standard logging to keep logs clean."""
        return

def run_server():
    """Run the health check server."""
    try:
        with socketserver.TCPServer(("", PORT), HealthCheckHandler) as httpd:
            logger.info(f"Health check server running on port {PORT}")
            httpd.serve_forever()
    except Exception as e:
        logger.error(f"Health check server error: {e}")

if __name__ == "__main__":
    run_server()
