import http.server
import hashlib
import cgitb
import re
import json
cgitb.enable()


def hash_message(string):
    d = hashlib.sha256()
    d.update(bytes(string, 'utf8'))
    digest = d.hexdigest()
    return digest


class LocalData(object):
    messages = {}
    stats = {}


class Handler(http.server.BaseHTTPRequestHandler):

    def parse_data(self):
        content_type = self.headers.get_content_type()
        if content_type == 'text/json':
            length = int(self.headers['content-length'])
            raw_data = self.rfile.read(length)
            data = json.loads(raw_data)
            message = data['message']
            if not message:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(bytes("ERROR: Message can't be empty\n", "utf8"))
                return False
        return message

    def do_GET(self):
        if re.search('/messages/([0-9]+|[a-f]+|[A-F]+)', self.path) is not None:
            hashed_message = self.path.split('/')[-1]
            if hashed_message not in LocalData.messages:
                self.send_response(404)
                self.send_header('Content-type', 'text/json')
                self.end_headers()
                get_response = bytes(f'{{\n  "error": "Unable to find message"\n  "message_sha256": "{hashed_message}"\n}}\n', "utf8")
                self.wfile.write(get_response)
                return

            decoded_message = LocalData.messages[hashed_message]
            print(f"message '{decoded_message}' found.")
            self.send_response(200)
            self.send_header('Content-type', 'text/json')
            self.end_headers()
            body = bytes(f'{{\n  "message": "{decoded_message}"\n}}\n', "utf8")
            self.wfile.write(body)

        elif self.path == '/metrics':
            pass
        else:
            self.send_response(403)
            self.send_header('Content-Type', 'text/json')
            self.end_headers()
        return

    def do_POST(self):
        if re.search('/messages', self.path) is not None:
            message = self.parse_data()
            if message:
                hashed = hash_message(message)
                LocalData.messages[hashed] = message
                print(f"message saved successfully as {hashed}")
                self.send_response(200)
                self.end_headers()
                post_response = bytes(f'{{\n  "digest": "{hashed}"\n}}\n', "utf8")
                self.wfile.write(post_response)
        else:
            self.send_response(403)
            self.send_header('Content-Type', 'text/json')
            self.end_headers()
        return


httpd = http.server.HTTPServer(('0.0.0.0', 8080), Handler)
httpd.serve_forever()
