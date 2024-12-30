from flask import Flask, render_template, request, redirect, url_for, session
from backend.session import SessionManager

app = Flask(__name__)
app.secret_key = "8820"  # Replace with a secure random key

# Session manager instance
session_manager = SessionManager()

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if session_manager.login(username, password):
            session["user"] = username
            return redirect(url_for("dashboard"))
        else:
            return "Invalid credentials. Please try again."
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))

@app.route("/dashboard")
def dashboard():
    if "user" in session:
        return render_template("dashboard.html", user=session["user"])
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
