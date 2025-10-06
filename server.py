from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import os
import mimetypes
import sqlite3
import http.cookies
import secrets
import json

SESSIONS = {}  # session_id -> username
TRAIT_TO_STONE = {
    frozenset({"artistic","reliable"}): "Amethyst",
    frozenset({"reliable", "confident"}): "Basalt",
    frozenset({"artistic", "confident"}): "Diamond",
    frozenset({"friendly", "confident"}): "Emerald",
    frozenset({"reliable", "tough"}): "Lapis Lazuli",
    frozenset({"friendly", "artistic"}): "Marble",
    frozenset({"tough", "confident"}): "Obsidian",
    frozenset({"tough", "reliable"}): "Quartz",
    frozenset({"friendly", "reliable"}): "Sandstone",
    frozenset({""}): "Turquoise",

    # ... etc for all combos
}

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):   
        # Cookie handling
        cookies = http.cookies.SimpleCookie(self.headers.get("Cookie"))
        session_id = cookies.get("session_id")

        if session_id and session_id.value in SESSIONS:
            username = SESSIONS[session_id.value]
            print(f"User {username} is logged in with session {session_id.value}")
            self.send_response(200)
        else:
            print("No valid session found")
            self.send_response(200)

        # Default to index.html
        path = self.path.lstrip("/")
        if path == "":
            path = "index.html"

        if os.path.isfile(path):
            # Guess MIME type (e.g. text/html, text/css)
            mime, _ = mimetypes.guess_type(path)
            if not mime:
                mime = "application/octet-stream"

            with open(path, "rb") as f:
                content = f.read()

            self.send_response(200)
            self.send_header("Content-type", mime)
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_error(404, "File Not Found")

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode()
        data = urllib.parse.parse_qs(body)

        # Parse cookies
        cookies = http.cookies.SimpleCookie(self.headers.get("Cookie"))

        username = data.get("username", [""])[0]
        email = data.get("email", [""])[0]
        password = data.get("password", [""])[0]
        password_again = data.get("password_again", [""])[0]

        if self.path == "/signup":
            success, msg = handle_signup(username, email, password, password_again)
            if success:
                # Create session
                sid = secrets.token_hex(16)
                SESSIONS[sid] = username
                print(f"User {username} signed up with session {sid}")
                self.send_response(302)  # redirect
                print("Redirecting to /stones.html")
                self.send_header("Location", "/stones.html")
                print("Redirect header sent")
                self.send_header("Set-Cookie", f"session_id={sid}; HttpOnly; Path=/")
                self.end_headers()
            else:
                self.respond_with_message(msg, status=401)
        
        elif self.path == "/home":
            sid = cookies.get("session_id")
            if sid and sid.value in SESSIONS:
                self.send_response(302)
                self.send_header("Location", "/home.html")
                self.end_headers()
            else:
                self.send_response(302)
                self.send_header("Location", "/index.html")
                self.end_headers()

        elif self.path == "/login":
            print(f"Login attempt for user: {username} with password: {password}")
            success, msg = handle_login(username, password)
            if success:
                sid = secrets.token_hex(16)
                SESSIONS[sid] = username

                self.send_response(302)
                self.send_header('Location', '/home.html')
                self.send_header("Set-Cookie", f"session_id={sid}; HttpOnly; Path=/")
                self.end_headers()                
            else:
                self.send_response(401)
                self.end_headers()

        elif self.path == "/logout":
            sid = cookies.get("session_id")
            if sid and sid.value in SESSIONS:
                del SESSIONS[sid.value]

            self.send_response(302)
            self.send_header("Location", "/index.html")
            self.send_header("Set-Cookie", "session_id=; Expires=Thu, 01 Jan 1970 00:00:00 GMT; Path=/")
            self.end_headers()
        
        elif self.path == "/check-signup":
            sid = cookies.get("session_id")
            if sid and sid.value in SESSIONS:
                print("User is logged in, redirecting to home.html")
                self.send_response(302)
                self.send_header("Location", "/home.html")
                self.end_headers()
            else:
                print("User not logged in, staying on signup page")
                self.send_response(302)
                self.send_header("Location", "/signup.html")  # or /login.html based on context
                self.end_headers()
        
        elif self.path == "/check-login":
            sid = cookies.get("session_id")
            if sid and sid.value in SESSIONS:
                print("User is logged in, redirecting to home.html")
                self.send_response(302)
                self.send_header("Location", "/home.html")
                self.end_headers()
            else:
                print("User not logged in, staying on login page")
                self.send_response(302)
                self.send_header("Location", "/login.html")  # or /signup.html based on context
                self.end_headers()

        elif self.path == "/evaluate_traits":

            traits = data.get("traits", [])
            print(f"Received traits: {traits}")
            if len(traits) != 2:
                self.send_error(400, "Must pick exactly two traits")
                return

            stone = TRAIT_TO_STONE.get(frozenset(traits), "Quartz")

            print(f"User with traits {traits} gets stone {stone}")
            print("Getting cookies...")
            sid = cookies.get("session_id")
            if sid and sid.value in SESSIONS:
                print("Found session, updating stone preference...")
                username = SESSIONS[sid.value]
                conn = sqlite3.connect("users.db")
                c = conn.cursor()
                c.execute("UPDATE users SET rock_group = ? WHERE username = ?", (stone, username))
                conn.commit()
                conn.close()
                self.respond_with_message(f"Stone preference updated to {stone}")
            else:
                self.respond_with_message("Not logged in", status=401)

            self.send_response(302)
            self.send_header("Location", "/home.html")
            self.end_headers()  

        elif self.path == "/guest":
            self.send_response(302)
            self.send_header("Location", "index.html")
            self.end_headers()

        elif self.path == "/api/stone":
            sid = cookies.get("session_id")
            if sid and sid.value in SESSIONS:
                print("Fetching stone preference for logged-in user...")
                username = SESSIONS[sid.value]
                conn = sqlite3.connect("users.db")
                conn.row_factory = sqlite3.Row
                c = conn.cursor()
                c.execute("PRAGMA foreign_keys = ON;")
                user = c.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
                conn.close()
                print(f"Fetched user from DB: {user["rock_group"]}")
                if user and user["rock_group"]:
                    stone = user["rock_group"]
                    response = json.dumps({"stone": stone})
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(response.encode())
                
                else:
                    self.send_response(404)
                    print(f"No stone preference found for user {user["username"]}")
                    self.end_headers()
            else:
                self.send_response(401)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Not logged in"}).encode())
                

               
    
    def respond_with_message(self, message, status=200):
        return
        self.send_response(status)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(message.encode())

def handle_signup(username, email, password, password_again):
    conn = sqlite3.connect("users.db")
    print("Connected to database for signup")
    c = conn.cursor()
    conn.execute("PRAGMA foreign_keys = ON;")
    if password != password_again:
        
        return False, "Passwords do not match"

    try:
        c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
        conn.commit()
        print(f"User {username} signed up successfully")
        return True, "Signup successful"
    except sqlite3.IntegrityError:
        print("Signup failed: username or email already exists")
        print(f"Username: {username}, Email: {email}")
        return False, "Username or email already exists"
    finally:
        print("Closing database connection after signup")
        conn.close()

def handle_login(username, password):
    print(f"Attempting login for user: {username} with password: {password}")
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys = ON;")

    user = c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password)).fetchone()
    conn.close()

    if user:
        print(f"User {username} logged in successfully")
        return True, f"Welcome back, {username}!"
    else:
        return False, "Invalid username or password"


    
        
if __name__ == "__main__":
    with sqlite3.connect("users.db") as conn:
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.row_factory = sqlite3.Row
        conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL,
            rock_group TEXT       
        )
        """)

=======
    server = HTTPServer(("127.0.0.1", 80), MyHandler)
    print("Server running at http://127.0.0.1:80")
>>>>>>> fb5ec0b (popup sidebar)
    server.serve_forever()
