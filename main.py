from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from supabase import create_client, Client
import os

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "super-secret-123")
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

SUPABASE_URL = "https://nrgxbagmrsybhsipjqxl.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5yZ3hiYWdtcnN5YmhzaXBqcXhsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDg0NTg2MDMsImV4cCI6MjA2NDAzNDYwM30.DmHlc3w2gaZABcu58uFO_j2LeiYHkw7i1mzrfNxCOwE"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route("/")
def index():
    if "user" in session:
        return redirect("/dashboard")
    return render_template("index.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        try:
            supabase.auth.sign_up({"email": email, "password": password})
            return redirect("/login")
        except Exception as e:
            return f"Signup error: {str(e)}"
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        try:
            user = supabase.auth.sign_in_with_password({"email": email, "password": password})
            if user.user:
                session["user"] = user.user.id
                return redirect("/dashboard")
            else:
                return "Login failed."
        except Exception as e:
            return f"Login error: {str(e)}"
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")
    return render_template("dashboard.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))