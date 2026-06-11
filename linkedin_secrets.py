import os
import sys
import webbrowser
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
from textwrap import dedent
import requests

# Configuration Settings
CLIENT_ID = "77qv8wo9i2oyad"
CLIENT_SECRET = os.getenv("LNKDIN_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:28003/lnkdin_oauth2/"
PORT = 28003

# Variable to hold the authorization code captured by the server
auth_code = None

# Local HTTP Server to intercept the LinkedIn redirect
class OAuthCallbackHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        global auth_code
        query_components = parse_qs(urlparse(self.path).query)

        if "code" in query_components:
            auth_code = query_components["code"][0]
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            # Inform the user in the browser window
            self.wfile.write(dedent("""\
                <!doctype html>
                <html>
                <body>
                
                <h1>Authorization successful!</h1>
                <p>You can close this window and return to your terminal.</p>
                
                </body>
                </html>\
            """).encode("utf-8"))
        else:
            self.send_response(400)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(dedent("""\
                <!doctype html>
                <html>
                <body>
                
                <h1>Authorization failed...</h1>
                <p>Re-run <code>linkedin_secrets.py</code> and try again.</p>
                
                </body>
                </html>\
            """).encode("utf-8"))

    def log_message(self, format, *args):
        return  # Suppress standard HTTP logging to keep terminal clean


def get_tokens(code):
    """Exchanges authorization code for access token and retrieves member URN."""
    # Exchange code for Access Token
    token_url = "https://www.linkedin.com/oauth/v2/accessToken"
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }

    token_response = requests.post(token_url, data=payload)
    token_data = token_response.json()

    if "access_token" not in token_data:
        print("\x1b[1;31mError fetching access token:\x1b[0m", token_data)
        sys.exit(1)

    access_token = token_data["access_token"]

    # Fetch the User Profile to extract Member URN
    profile_url = "https://api.linkedin.com/v2/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}
    profile_response = requests.get(profile_url, headers=headers)
    profile_data = profile_response.json()

    if "sub" not in profile_data:
        print("\x1b[1;31mError fetching profile URN:\x1b[0m", profile_data)
        sys.exit(1)

    member_urn = f"urn:li:person:{profile_data['sub']}"

    # Output data for GitHub Secrets
    print("\x1b[1;32msuccess!\x1b[0m\n")
    print("\x1b[1m" + " Quickly copy this value to GitHub Repo Secrets: ".center(80, "=") + "\x1b[0m")
    print(f"\x1b[1mLNKDIN_ACCESS_TOKEN\x1b[0m = {access_token}\n")
    print("\x1b[1;33mThe access token will expire after 60 days. That means "
          "you will have to run this script again after 60 days.\x1b[0m")
    
    with open("linkedin_urn.config.txt", "w") as f:
        print(member_urn, file=f)
    
    print("\n\x1b[1;32mWrote URN to linkedin_urn.config.txt\x1b[0m")


def main():
    # Start the local server
    server = HTTPServer(("localhost", PORT), OAuthCallbackHandler)

    # Build the authorization login link
    scopes = "openid profile w_member_social"
    auth_url = f"https://www.linkedin.com/oauth/v2/authorization?client_id=" \
               f"{CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope={scopes}" \
               f"&response_type=code"

    print(f"Starting local server on port {PORT}...")
    print("Opening your browser to authorize application... ", end="")

    # Automatically launch default system browser
    webbrowser.open(auth_url)

    # Wait for exactly one incoming request, process it, then exit the loop
    server.handle_request()
    server.server_close()

    if auth_code:
        print("\x1b[1;32msuccess!\x1b[0m\nIntercepted authorization code. Requesting tokens... ", end="")
        get_tokens(auth_code)
    else:
        print("\x1b[1;31mFailed to catch authorization code.\x1b[0m")

if __name__ == "__main__":
    main()