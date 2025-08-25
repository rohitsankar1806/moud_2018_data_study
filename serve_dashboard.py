#!/usr/bin/env python3
"""
Simple HTTP server to serve the MOUD dashboard
"""

import http.server
import socketserver
import webbrowser
import os
from pathlib import Path

def serve_dashboard(port=8000):
    """Serve the dashboard on localhost"""
    os.chdir(Path(__file__).parent)
    
    class CustomHandler(http.server.SimpleHTTPRequestHandler):
        def end_headers(self):
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            super().end_headers()
    
    try:
        with socketserver.TCPServer(("", port), CustomHandler) as httpd:
            print(f"✓ MOUD Dashboard Server started")
            print(f"🌐 Open your browser to: http://localhost:{port}")
            print(f"📊 Dashboard file: {Path.cwd() / 'index.html'}")
            print(f"📈 Data file: {Path.cwd() / 'dashboard_data.json'}")
            print("\nPress Ctrl+C to stop the server")
            
            # Try to open browser automatically
            try:
                webbrowser.open(f'http://localhost:{port}')
                print("🚀 Opening dashboard in your default browser...")
            except:
                pass
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n👋 Dashboard server stopped")
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Port {port} is already in use. Try a different port:")
            print(f"   python3 serve_dashboard.py --port {port + 1}")
        else:
            print(f"❌ Server error: {e}")

if __name__ == "__main__":
    import sys
    port = 8000
    
    # Simple argument parsing
    if len(sys.argv) > 1 and sys.argv[1] == "--port" and len(sys.argv) > 2:
        try:
            port = int(sys.argv[2])
        except ValueError:
            print("Invalid port number")
            sys.exit(1)
    
    serve_dashboard(port)