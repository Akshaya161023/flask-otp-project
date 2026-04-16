from flask import Flask, render_template, request, session, redirect, url_for
from otp_utils import generate_otp, verify_otp
from email_sender import send_otp_email
import os
from database import register_user, user_exists, get_user

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# --- Login page (choose register or login) ---
@app.route("/")
def home():
    return render_template("login.html")

# --- Registration ---
@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        success, msg = register_user(name, email)
        if not success:
            error = msg
        else:
            session["email"] = email
            session["name"] = name
            otp = generate_otp(email)
            send_otp_email(email, otp)
            return redirect(url_for("verify"))
    return render_template("register.html", error=error)

# --- Login ---
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        email = request.form["email"]
        if not user_exists(email):
            error = "Email not registered. Please register first."
        else:
            session["email"] = email
            user = get_user(email)
            session["name"] = user["name"]
            otp = generate_otp(email)
            send_otp_email(email, otp)
            return redirect(url_for("verify"))
    return render_template("login.html", error=error)

# --- OTP verification ---
@app.route("/verify", methods=["GET", "POST"])
def verify():
    result = None
    if request.method == "POST":
        email = session.get("email")
        user_otp = request.form["otp"]
        if verify_otp(email, user_otp):
            return redirect(url_for("success"))
        else:
            result = "wrong"
    return render_template("verify.html", result=result)


# --- Success page ---
@app.route("/success")
def success():
    name = session.get("name", "User")
    email = session.get("email", "")
    return render_template("success.html", name=name, email=email)

if __name__ == "__main__":
    app.run(debug=True)