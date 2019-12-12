from problem_parser import Problem
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from os import listdir
from os.path import isfile, join

#Read problems from directory
problem_directory = "problems"
files = [f for f in listdir(problem_directory) if isfile(join(problem_directory, f))]
problems = {p: Problem.from_file(join(problem_directory, p)) for p in files if p.endswith(".txt")}

class ProblemServer(BaseHTTPRequestHandler):
    def _set_response(self, content):
        self.send_response(200)
        self.send_header("content-type", content)
        self.end_headers()

    def _send(self, data):
        self.wfile.write(data.encode("utf-8"))

    def _read(self):
        content_length = int(self.headers["Content-Length"])
        return self.rfile.read(content_length).decode("utf-8")

    def do_GET(self):
        if self.path == "/available":
            self._set_response("application/json")
            self._send(json.dumps(list(problems.keys())))
        elif self.path[1:] in problems.keys():
            prob = problems[self.path[1:]]
            self._set_response("text/plain")
            self._send(prob.statment())
        else:
            self._set_response("text/html")
            with open("index.html", "r") as f:
                self._send(f.read())

    def do_POST(self):
        user_code = self._read()
        prob = problems[self.path[1:]]
        correct = prob.execute(user_code)
        
        self._set_response("application/json")
        self._send(json.dumps(correct))


PORT = 8080

with HTTPServer(("", PORT), ProblemServer) as httpd:
    print(PORT)
    httpd.serve_forever()
