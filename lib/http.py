from http.server import BaseHTTPRequestHandler


class Server(BaseHTTPRequestHandler):
    def response(self, code, content_type, body):
        self.send_response(code)
        self.send_header("Content-type", content_type)
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))

    def redirect(self, location):
        body = f"""
        <!DOCTYPE html>
        <html lang="en">
          <head>
            <meta charset="utf-8">
            <title>Redirecting&hellip;</title>
            <meta http-equiv="refresh" content="0; url={location}" />
            <script>location="{location}"</script>
            <meta name="robots" content="noindex">
          </head>
          <body>
            <h1>Redirecting&hellip;</h1>
            <p>
              This page has moved to
              <a href="{location}">{location}</a>.
            </p>
          </body>
        </html>
        """
        self.send_response(302)
        self.send_header("Location", location)
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))
