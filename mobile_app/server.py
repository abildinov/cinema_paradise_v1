import http.server
import socketserver
import os

PORT = 3001

class NoCacheHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Добавляем заголовки для отключения кэширования
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()
    
    def do_GET(self):
        # Если запрашивается корень, перенаправляем на index.html
        if self.path == '/':
            self.path = '/index.html'
        super().do_GET()

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    with socketserver.TCPServer(("", PORT), NoCacheHTTPRequestHandler) as httpd:
        print(f"📱 Сервер запущен на http://localhost:{PORT}")
        print(f"📱 Без кэширования! Обновляет файлы автоматически.")
        httpd.serve_forever() 