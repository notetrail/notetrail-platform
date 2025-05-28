from flask import Flask, request, redirect, session
from flask_session import Session
from supabase import create_client, Client
import os

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "super-secret-123")
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://nrgxbagmrsybhsipjqxl.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5yZ3hiYWdtcnN5YmhzaXBqcXhsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDg0NTg2MDMsImV4cCI6MjA2NDAzNDYwM30.DmHlc3w2gaZABcu58uFO_j2LeiYHkw7i1mzrfNxCOwE")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route("/")
def index():
    if "user" in session:
        return redirect("/dashboard")
    return "<a href='/signup'>Sign Up</a> | <a href='/login'>Log In</a>"

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        supabase.auth.sign_up({"email": email, "password": password})
        return redirect("/login")
    return """
    <h2>Sign Up</h2>
    <form method="post">
      Email: <input name="email"><br>
      Password: <input name="password" type="password"><br>
      <input type="submit" value="Sign Up">
    </form>
    """

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = supabase.auth.sign_in_with_password({"email": email, "password": password})
        session["user"] = user.user.id
        return redirect("/dashboard")
    return """
    <h2>Log In</h2>
    <form method="post">
      Email: <input name="email"><br>
      Password: <input name="password" type="password"><br>
      <input type="submit" value="Log In">
    </form>
    """

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")
    return "<h2>Welcome to your dashboard!</h2><br><a href='/logout'>Log Out</a>"

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")