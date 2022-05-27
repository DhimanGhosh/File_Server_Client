from http.server import SimpleHTTPRequestHandler
import socketserver

server = socketserver.TCPServer(('', 80), SimpleHTTPRequestHandler)
print('Server running on port: 80\nPlease Visit: http://127.0.0.1:80')
server.serve_forever()
